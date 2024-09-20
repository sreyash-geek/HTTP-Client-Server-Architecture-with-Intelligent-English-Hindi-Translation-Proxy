# Import necessary modules
from socket import *
import threading
import re

# Create a server socket, bind it to a specific IP address and port, and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(('127.0.0.1', 35000))
tcpSerSock.listen()

# Set the socket option to allow reusing the address
tcpSerSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

try:

    # Define a function to handle incoming client connections
    def handle_clients(tcpCliSock, addr):

        # Receive the HTTP request message from the client
        message = tcpCliSock.recv(4096).decode()
        print(f"Received request from a client {addr}: ", message)

        hostname = None

        # Extract the hostname and port number from the client's request using regular expressions
        message_parsed = re.search('Host: (.)+(:[0-9]{1,5})?', message)
        if message_parsed:
            hostname = message_parsed.group(0)[6:]

        try:
            # Split the hostname into address and port parts
            host_port_parts = hostname.split(':')
            if len(host_port_parts) == 2:
                addr, portno = host_port_parts
            else:
                addr = hostname.replace("\r", "")
                portno = 80

            connect_to_server = (addr, int(portno))

        except ValueError as e:
            # If there's an error, set a default port number and address
            connect_to_server = (hostname.replace("\r", ""), 80)

        # Create a socket for connecting to the main web server
        tcpproxyclient = socket(AF_INET, SOCK_STREAM)
        tcpproxyclient.settimeout(3)

        # Connect to the main web server using the extracted address and port
        tcpproxyclient.connect(connect_to_server)
        print("...Sending request to the main web server...")

        # Send the client's request to the main web server
        tcpproxyclient.sendall(message.encode())

        response_from_server = None

        try:
            while True:
                # Receive the server's response
                response_from_server = tcpproxyclient.recv(4096)
                if not response_from_server:
                    break

                # Send the server's response back to the client
                tcpCliSock.sendall(response_from_server)

        except socket.timeout:
            pass

        finally:
            # Close the client's connection and the connection to the main web server
            tcpCliSock.close()
            tcpproxyclient.close()

    while True:
        # Start receiving data from the client
        print('...Proxy Server is ready to serve...')
        tcpCliSock, addr = tcpSerSock.accept()
        print('Received a connection from: ', addr)

        # Create a thread for each client to handle their requests concurrently
        proxy_server_thread = threading.Thread(target=handle_clients, args=(tcpCliSock, addr))
        proxy_server_thread.start()

except KeyboardInterrupt:
    # Close the server socket and terminate the program on keyboard interrupt
    tcpSerSock.close()
    print("\nConnection Terminated\n")
