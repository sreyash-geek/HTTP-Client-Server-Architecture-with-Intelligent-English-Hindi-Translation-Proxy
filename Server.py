# Import necessary modules
from socket import *
import threading
import re

# Create a server socket, bind it to a specific IP address and port, and start listening
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('127.0.0.1', 10000))
serverSocket.listen()

# Define a function to handle incoming client connections
def handle_clients(connectionSocket, addr):
    print(f"...Client with IP address {addr} has connected...")

    try:
        # Receive the HTTP request message from the client
        message = connectionSocket.recv(4096).decode()

        # Use a regular expression to parse the client's GET request
        message_parsed = re.search('^GET /([a-zA-Z0-9\.%/_-]+)', message)
        if message_parsed:
            filename = message_parsed.group(1)
        else:
            filename = "index.html"  # Use a default file if no specific file is requested

        # Determine the content type based on the requested file's extension
        if filename.endswith(".html"):
            content_type = "text/html"
        elif filename.endswith(".ico"):
            content_type = "image/x-icon"
        elif filename.endswith(".jpg"):
            content_type = "image/jpeg"
        elif filename.endswith(".css"):
            content_type = "text/css"
        elif filename.endswith(".js"):
            content_type = "application/javascript"

        try:
            # Open and read the requested file
            with open(filename, 'rb') as f:
                outputdata = f.read()

            # Send a valid HTTP response with headers and content
            response = f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\n\r\n".encode() + outputdata
            connectionSocket.send(response)
            print(f"...Connection with {addr} served...")

        except IOError:
            # Send a 404 Not Found response if the requested file is not found
            response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\nFile Not Found"
            connectionSocket.send(response.encode())
            print(f"...Connection with {addr} could not be served...")

    finally:
        # Close the client's connection
        connectionSocket.close()
        print(f"...Connection with {addr} closed...")

# Continuously listen for client connections and create threads to handle them
while True:
    print('...Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    server_thread = threading.Thread(target=handle_clients, args=(connectionSocket, addr))
    server_thread.start()
