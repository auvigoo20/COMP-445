import socket
import threading
import os
import argparse
from httpfs_library import build_response_from_request

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


parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('--help', dest='help', action='store_true')
parser.add_argument('-v', dest='verbose', action='store_true')
parser.add_argument('-p', dest='port', default=8080)
parser.add_argument('-d', dest='path_to_dir', default=current_directory)
args = parser.parse_args()
run_server('', int(args.port))
