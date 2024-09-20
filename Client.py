# Import necessary modules
from socket import *
import sys

# Check if the correct number of command line arguments are provided
if len(sys.argv) != 4 and len(sys.argv) != 6:
    print("Usage: python3 http_web_client.py <hostname> <server_port> <path> or python http_web_client.py <hostname> <server_port> <path> <proxy_port> <proxy_addr>")
    sys.exit(1)

# Retrieve command line arguments for hostname, server port, and path
hostname = sys.argv[1]
port = int(sys.argv[2])
path = sys.argv[3]

# Combine hostname and port to create the server identifier
hostname += ":" + str(port)

# Check if a proxy server is specified
if len(sys.argv) == 6:
    proxy_port = sys.argv[4]
    proxy_server = sys.argv[5]
    server = (proxy_server, int(proxy_port))  # Create a tuple for the proxy server

elif len(sys.argv) == 4:
    server = (hostname, port)  # Create a tuple for the direct web server

print(server)

try:
    # Create a socket object for the client
    recv_client_socket = socket(AF_INET, SOCK_STREAM)

    # Connect to the web server or proxy
    recv_client_socket.connect(server)

    # Construct the HTTP request
    http_request = f"GET {path} HTTP/1.1\r\nHost: {hostname}\r\n\r\n"

    print(http_request)

    # Send the HTTP request to the server or proxy
    recv_client_socket.send(http_request.encode())

    # Receive and store the response from the server
    response_from_server = ""

    while True:
        received_data = recv_client_socket.recv(4096).decode()
        if not received_data:
            break
        response_from_server += received_data

    print(response_from_server)

    # Close the socket
    recv_client_socket.close()

except Exception as e:
    print("\nAn Error occurred\n")
    # Close the socket in case of an exception
    recv_client_socket.close()
