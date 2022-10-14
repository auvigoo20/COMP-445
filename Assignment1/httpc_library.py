import socket
from urllib.parse import urlparse


def build_http_request(url, command, headers, data, file):
    parsed_URL = urlparse(url)
    host = parsed_URL.netloc
    path = parsed_URL.path if len(parsed_URL.path) > 0 else "/"
    query = parsed_URL.query

    request = ""

    if command == 'get':
        # Build the GET request
        request = "GET " + path

        # Append query params
        if len(query) > 0:
            request = request + "?" + query

        # Append host
        request = request + " HTTP/1.0\r\nHost:" + host + "\r\n" + "User-Agent:Concordia-HTTP/1.0\r\n"

        # Append headers
        if headers:
            for header in headers:
                request = request + header + "\r\n"

        request = request + "\r\n"
    elif command == 'post':
        # Build the POST request
        request = "POST " + path

        # Append query params
        if len(query) > 0:
            request = request + "?" + query

        # Append host and user agent
        request = request + " HTTP/1.0\r\nHost:" + host + "\r\n" + "User-Agent:Concordia-HTTP/1.0\r\n"

        # Append headers
        if headers:
            for header in headers:
                request = request + header + "\r\n"

        # Append inline data
        if data:
            request = request + "Content-Length:" + str(len(data)) + "\r\n\r\n" + data

        # Append file data
        if file:
            file = open(file, "r")
            try:
                file_content = file.read()
                request = request + "Content-Length:" + str(len(file_content)) + "\r\n\r\n" + file_content
            except Exception as e:
                print(f"An error has occured when reading the file:{e}")
            finally:
                file.close()

        request = request + "\r\n"

    return request


def send_request(host, request, port):
    # Connect to host
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    # Encode and send request
    request_encoded = request.encode("utf-8")
    sock.send(request_encoded)

    # Receive and decode response
    response_encoded = sock.recv(1024)
    response = response_encoded.decode("utf-8")
    sock.close()
    return response
