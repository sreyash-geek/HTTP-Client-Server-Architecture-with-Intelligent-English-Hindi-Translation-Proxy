
# ACN PROGRAMMING ASSIGNMENT - 2 WWW

The purpose of this www assignment was to learn about Web clients, Web servers, Web proxies, and the HyperText Transfer Protocol (HTTP). 

The report is a brief explanation on 4 parts broadly:

### Part 1: 

Implementation of basic web client.

### Part 2:

Implementation of basic web server. 

### Part 3:

Implementation of basic web proxy.


### Part 4:  

Extension to Part 1 mentioned in detail below.


## PART-1: A Simple Web Client 

In this part, we develop a simple web client which will connect to the web server directly or through the intermediate web proxy using a TCP connection, send HTTP requests to the server, and display the server responses as output. The client takes variable number of command line arguments specifying the IP address of the web proxy, host name or IP address of the web server, the port at which the proxy and web server are listening in case of indirect connection through the web proxy or simply IP address and port at which the web server is listening in case of direct connection to the web server and the path at which the requested object is stored at the web server. 


## PART-2: A Simple Web Proxy Server
In this part, we implemented and tested a simple Web proxy. This web proxy performs the first role (proxying) but not the second role (caching). The goal is to build a properly functioning Web proxy for simple web pages.
The most important HTTP command for your web proxy to handle is the "GET" request, which specifies the URL for an object to be retrieved. In the basic operation of your proxy, it should be able to parse, understand, and forward to the Web server a (possibly modified) version of the client request. Similarly, the proxy should be able to parse, understand, and return to the client a (possibly modified) version of the response that the Web server provided to the proxy. Your proxy should be able to handle response codes such as 200 (OK) and 404 (Not Found) correctly, notifying the client as appropriate. We implemented 2 TCP (stream) sockets for client-server communication, one for client-proxy communication and the other for proxy-server communication. The proxy handles multiple clients using multi-threading. 


NOTE: The Proxy only serves HTTP requests correctly and doesn’t handle the case for HTTPS.


### PART-3: A Simple Web Server
In this part, we developed a multi-threaded web server that handles multiple HTTP requests simultaneously from your own web client(s) (PART-1), web browsers and your own proxy server (PART-2). Using threading, we create a main thread in which the modified server listens for clients at a fixed port. When it receives a TCP connection request from a client, it will set up the TCP connection through another port and service the client request in a separate thread. There will be a separate TCP connection in a separate thread for each HTTP request/response pair. Each thread at the web server accepts and parses the HTTP request, gets the requested file from the server’s file system, creates an HTTP response message consisting of the requested file preceded by header lines, and then sends the response directly to the client. If the requested file is not present in the server, it sends a HTTP “404 Not Found” message back to the client.

Files in the Server directory:
index.html
style.css

### PART-4: Extension to Proxy-Server in PART-2:

English to Hindi Web Page Translation and web usage stats at web proxy: 
Users can URLs of English language web pages and get displayed web page content in Hindi language in the browser. So, Proxy has to accept URL requests from the web browser, gets the response from the respective web server, translates the response message to Hindi or any other Indian language using an open-source translation library (deep-translator) by Google, and sends the translated page to the web browser. 

Web usage Statistics: Here proxy keeps track of users browsing activities, i.e., links they are visiting. You could use MAC or IP addresses to classify links to any particular user. Finally, the proxy provides aggregate web usage statistics on a daily/weekly/monthly basis in terms of pie charts, bar graphs, etc.  




## Running Tests

To run web client, go run the following command:

```bash
   python3 Client.py <hostname> <server_port> <path> <proxy_port> <proxy_addr>
```
or

```bash
   python3 Client.py <hostname> <server_port> <path> 
```

To run web-server:

```bash
   python3 Server.py
```

To run web-proxy:


```bash
   python3 Proxy.py
```

To run extended-proxy:


```bash
   python3 ExtendedProxy.py
```


### NOTE 

The following codes are configured to run on the local machines (127.0.0.1), this could be run on any machine using the client's IP address.


If web-browser is being used as the client, then the url could use HTTP requests of the form:

http://www.example.com 

or 

www.example.com

Make sure to configure the browser to send the requests through your proxy server to destination, in case of browserbeing used as the web client.

The codes don't handle HTTPS requests. 


## Acknowledgements

 https://en.wikipedia.org/wiki/Proxy_server
https://gaia.cs.umass.edu/kurose_ross/programming/Python_code_only/Web_Proxy_programming_only.pdf
https://gaia.cs.umass.edu/kurose_ross/programming/Python_code_only/WebServer_programming_lab_only.pdf
HTTP 1.1 RFC: http://tools.ietf.org/html/rfc2616
https://web.mit.edu/6.033/2000/www/lab/webproxy.html
Sockets Tutorial: http://www.linuxhowtos.org/C_C++/socket.htm
Beej's Guide to Network Programming Using Internet Socket: https://www.beej.us/guide/bgnet/     	
Programming UNIX Sockets in C - Frequently Asked Questions: http://www.softlab.ntua.gr/facilities/documentation/unix/unix-socket-faq/unix-socket-faq.html
 



## Usage/Configurations

```bash
Proxy IP address : 127.0.0.1
Proxy Port no. : 35000
Server IP address : 127.0.0.1
Server Port no. : 80 (Default)
                      or
                  10000 (Local)
Extended Proxy Port IP address : 127.0.0.1
Extended Proxy Port no. : 37000                  
```                  

These are the configurations to run codes simultaneously in case of direct and indirect connections.                 


