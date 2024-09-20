# Import necessary libraries
from socket import *
import threading
import re
import csv
import matplotlib.pyplot as plt
import time
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
import pandas as pd

# Create a server socket, bind it to an IP address and port, and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(('127.0.0.1', 37000))
tcpSerSock.listen(5)

# Initialize a dictionary to track user activity
user_activity = {}

# Initialize the CSV file for web usage statistics with headers
with open('web_usage_stats.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Date', 'IP', 'Domain', 'Visits'])

try:
    # Function to generate a bar plot for domain-wise statistics
    def generate_domain_wise_bar(data_file):
        # Read the CSV file into a DataFrame
        df = pd.read_csv(data_file)

        # Group the data by domain and sum the visits
        domain_visits = df.groupby('Domain')['Visits'].sum()

        # Generate a bar plot
        plt.figure(figsize=(12, 6))
        domain_visits.plot(kind='bar', title='Visits / Domain')
        plt.xlabel('Domain')
        plt.ylabel('Visits')
        plt.xticks(rotation=90)
        plt.show()

    # Function to generate a pie plot for domain-wise statistics
    def generate_domain_wise_pie(data_file):
        # Read the CSV file into a DataFrame
        df = pd.read_csv(data_file)

        # Count the number of unique domains visited
        domain_counts = df['Domain'].value_counts()

        # Generate a pie plot
        plt.figure(figsize=(8, 8))
        plt.pie(domain_counts, labels=domain_counts.index, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title('Domains Visited')
        plt.show()

    # Function to generate a bar plot for daily web usage statistics
    def generate_daily_stats_plot(data_file):
        df = pd.read_csv(data_file)
        df['Date'] = pd.to_datetime(df['Date'])
        daily_stats = df.groupby(['Date'])['Visits'].sum()

        daily_stats.plot(kind='bar', title='Daily Web Usage Statistics')
        plt.xlabel('Date')
        plt.ylabel('Visits')
        plt.show()

    # Function to translate HTML content
    def translate_html_content(doc):
        # Parse the HTML content
        soup = BeautifulSoup(doc, 'html.parser')

        # Find the elements or tags that you want to translate
        elements_to_translate = soup.find_all(['p', 'h1', 'li', 'a'])

        # Translate and replace text within selected elements
        for element in elements_to_translate:
            original_text = element.get_text()
            translated_text = GoogleTranslator(source='en', target='hi').translate(original_text)
            print(translated_text)
            element.string = translated_text

        # Get the modified HTML content
        modified_html = str(soup)

        return modified_html

    # Function to handle client requests
    def handle_clients(tcpCliSock, addr):
        # Receive the request message from the client
        message = tcpCliSock.recv(4096).decode()
        print(f"Received request from a client {addr}: {message}")

        # Extract client's IP and requested hostname
        client_ip = addr
        hostname = None
        message_parsed = re.search(r'Host: (.+)', message)
        if message_parsed:
            hostname = message_parsed.group(1)

        domain = hostname

        try:
            # Parse the hostname and port number
            host_port_parts = hostname.split(':')
            if len(host_port_parts) == 2:
                addr, portno = host_port_parts
            else:
                addr = hostname.replace("\r", "")
                portno = 80

            # Create a connection to the target web server
            connect_to_server = (addr, int(portno))

        except (ValueError, AttributeError) as e:
            print(f"Error parsing hostname: {e}")
            return

        # Create a socket for connecting to the target web server
        tcpproxyclient = socket(AF_INET, SOCK_STREAM)
        tcpproxyclient.connect(connect_to_server)

        # Update user activity dictionary
        if client_ip not in user_activity:
            user_activity[client_ip] = {}

        # Track domain visits
        if domain in user_activity[client_ip]:
            user_activity[client_ip][domain] += 1
        else:
            user_activity[client_ip][domain] = 1

        # Log the visit in the CSV file
        with open('web_usage_stats.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            for ip, domains in user_activity.items():
                for domain, visits in domains.items():
                    writer.writerow([time.strftime('%Y-%m-%d'), ip, domain, visits])

        print("Sending request to the main web server")

        # Send the client's request to the main web server
        tcpproxyclient.sendall(message.encode())

        # Receive and print the response from the main web server
        response_from_server = b""
        while True:
            received_data = tcpproxyclient.recv(4096)
            if not received_data:
                break
            response_from_server += received_data

        # Send the response back to the client
        tcpCliSock.sendall(response_from_server)

        print(response_from_server)

        # Decode the response content
        decoded_response = response_from_server.decode('utf-8', errors='ignore')

        print(decoded_response)

        # Split the response into headers and body
        response_parts = decoded_response.split('\r\n\r\n', 1)
        headers = response_parts[0]
        body = response_parts[1] if len(response_parts) > 1 else ""

        response_headers = headers

        print(headers)
        print("\n")
        print(body)

        # Check if the response content type is HTML
        if "Content-Type: text/html" in response_headers:
            translated_parsed_content = translate_html_content(body)
            new_content_length = len(translated_parsed_content)
            content_length_pattern = r'Content-Length: \d+'
            translated_parsed_content = re.sub(content_length_pattern, f'Content-Length: {new_content_length}', translated_parsed_content)
            new_http_response = response_headers + '\r\n\r\n' + translated_parsed_content
            print(new_http_response)
        else:
            # If content type is not HTML, print the response as-is
            print(decoded_response)

        # Close the sockets
        tcpCliSock.close()
        tcpproxyclient.close()

    while True:
        # Start receiving data from the client
        print('Proxy Server is ready to serve...')
        tcpCliSock, addr = tcpSerSock.accept()
        print('Received a connection from: ', addr)

        # Server creates a thread and passes a handle_client functionality to it, the function takes care of serving the client
        proxy_server_thread = threading.Thread(target=handle_clients, args=(tcpCliSock, addr))

        # Starting the threading process
        proxy_server_thread.start()

except KeyboardInterrupt:
    tcpSerSock.close()

    # Generate and display web usage statistics before exiting
    generate_daily_stats_plot('web_usage_stats.csv')
    generate_domain_wise_pie('web_usage_stats.csv')
    generate_domain_wise_bar('web_usage_stats.csv')
    print("\nConnection Terminated")
