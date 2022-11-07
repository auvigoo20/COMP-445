import socket
import threading
import datetime
import argparse

http_version = 'HTTP/1.1'


def run_server(host, port):
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        listener.bind((host, port))
        listener.listen(5)
        print('Httpfs server is listening at', port)
        while True:
            connection_socket, addr = listener.accept()
            threading.Thread(target=handle_client, args=(connection_socket, addr)).start()
    finally:
        listener.close()


def handle_client(conn, addr):
    print('New client from', addr)
    try:
        data = conn.recv(1024)
        request = data.decode("utf-8")
        print(request)

        request_sections = request.split("\r\n\r\n")
        request_header = request_sections[0]
        request_header_first_line = request_header.split('\r\n')[0].split(' ')
        request_body = ''
        if len(request_sections) > 1:
            request_body = request_sections[1]
        request_method = request_header_first_line[0]
        request_url = request_header_first_line[1]

        response_code = ''
        response_header = ''
        response_body = ''

        if request_method == 'GET':
            print('get request')
            response_code = '200 OK'
        elif request_method == 'POST':
            print('post request')
            response_code = '200 OK'

        now = datetime.datetime.now(datetime.timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')

        response_header = http_version + ' ' + response_code + '\r\nDate: ' + now
        response_header = response_header + '\r\nContent-Type: text\r\nContent-Length: ' + str(
            len(response_body)) + '\r\nConnection: close\r\nServer: httpfs\r\n\r\n '

        final_response = response_header + response_body

        conn.sendall(final_response.encode("utf-8"))
    finally:
        conn.close()


run_server('', 8080)
