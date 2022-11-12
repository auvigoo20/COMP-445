import socket
import threading
import datetime
import os
import argparse

http_version = 'HTTP/1.0'
current_directory = os.getcwd()


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

        # Set the directory of the file server if not default
        if not args.path_to_dir == current_directory:
            working_directory = os.path.abspath(current_directory + args.path_to_dir)
        else:
            working_directory = args.path_to_dir

        response = build_response_from_request(request, working_directory)
        conn.sendall(response.encode("utf-8"))

    finally:
        conn.close()


def build_response_from_request(request, server_directory):
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
        # Prevent the user from accessing files outside the working directory (for example Assignment2/testfolder/../..)
        request_url_absolute_path = os.path.abspath(server_directory + request_url)
        if not request_url_absolute_path.startswith(server_directory):
            response_code = '403 Forbidden'
        else:  # Check if path is invalid, a file or a directory
            if not os.path.exists(request_url_absolute_path):
                response_code = '404 Not Found'

            # GET /
            elif os.path.isdir(request_url_absolute_path):
                try:
                    list_of_files = os.listdir(request_url_absolute_path)
                    for i in list_of_files:
                        response_body = response_body + i + '\r\n'
                    response_code = '200 OK'
                except IOError:
                    response_code = '400 Bad request'

            # GET /foo
            elif os.path.isfile(request_url_absolute_path):
                try:
                    file_to_read = open(request_url_absolute_path)
                    response_body = response_body + file_to_read.read()
                    response_code = '200 OK'
                    file_to_read.close()
                except IOError:
                    response_code = '404 Not Found'
    elif request_method == 'POST':
        # Prevent the user from accessing files outside the working directory (for example
        # Assignment2/testfolder/../..)
        request_url_absolute_path = os.path.abspath(server_directory + request_url)
        if not request_url_absolute_path.startswith(server_directory):
            response_code = '403 Forbidden'
        else:
            try:
                file_to_write = open(request_url_absolute_path, 'w')
                file_to_write.write(request_body)
                response_code = '201 Created'
                file_to_write.close()
            except IOError:
                response_code = '404 Not Found'

    now = datetime.datetime.now(datetime.timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')
    response_header = response_header + http_version + ' ' + response_code + '\r\nDate: ' + now
    response_header = response_header + '\r\nContent-Type: text\r\nContent-Length: ' + str(
        len(response_body)) + '\r\nConnection: close\r\nServer: httpfs\r\n\r\n'

    final_response = response_header + response_body
    return final_response


parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('--help', dest='help', action='store_true')
parser.add_argument('-v', dest='verbose', action='store_true')
parser.add_argument('-p', dest='port', default=8080)
parser.add_argument('-d', dest='path_to_dir', default=current_directory)
args = parser.parse_args()
run_server('', int(args.port))
