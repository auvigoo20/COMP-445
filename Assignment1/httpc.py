import argparse
import socket
from urllib.parse import urlparse


def testrun():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "httpbin.org"

    sock.connect((host, 80))

    # GET only
    # line = "GET /?q=hello+world HTTP/1.0\r\nHost:google.ca\r\n\r\n"

    # GET with query params
    # line = "GET /get?course=networking&assignment=1 HTTP/1.0\r\nHost:httpbin.org\r\n\r\n"

    # POST with header and inline data
    someJSON = "{\"Assignment\":1}"
    line = "POST /post HTTP/1.0\r\nHost:httpbin.org\r\nContent-Type:application/json\r\n" + "Content-Length:" + str(
        len(someJSON)) + "\r\n\r\n" + someJSON + "\r\n"

    # POST with header and file
    # file = open("hello.txt", "r")
    # try:
    #     fileContent = file.read()
    #     line = "POST /post HTTP/1.0\r\nHost:httpbin.org\r\nContent-Type:application/json\r\n" + "Content-Length:" + str(
    #         len(fileContent)) + "\r\n\r\n" + fileContent + "\r\n"
    #
    # except Exception as e:
    #     print(f"An error has occured when reading the file:{e}")
    # finally:
    #     file.close()

    request = line.encode("utf-8")
    sock.send(request)

    response = sock.recv(1024)

    print(response.decode("utf-8"))

    sock.close()


help_general = ("httpc is a curl-like application but supports HTTP protocol only.\n"
                "Usage:\n"
                "httpc command [arguments]\n"
                "The commands are:\n"
                "\tget executes a HTTP GET request and prints the response.\n"
                "\tpost executes a HTTP POST request and prints the response.\n"
                "\thelp prints this screen.\n"
                "Use \"httpc help [command]\" for more information about a command.\n")

help_get = ("usage: httpc get [-v] [-h key:value] URL\n"
            "Get executes a HTTP GET request for a given URL.\n"
            "\t-v Prints the detail of the response such as protocol, status, and headers.\n"
            "\t-h key:value Associates headers to HTTP Request with the format 'key:value'.\n")

help_post = ("usage: httpc post [-v] [-h key:value] [-d inline-data] [-f file] URL\n"
             "Post executes a HTTP POST request for a given URL with inline data or from file.\n"
             "\t-v Prints the detail of the response such as protocol, status, and headers.\n"
             "\t-h key:value Associates headers to HTTP Request with the format 'key:value'.\n"
             "\t-d string Associates an inline data to the body HTTP POST request.\n"
             "\t-f file Associates the content of a file to the body HTTP POST request.\n"
             "Either [-d] or [-f] can be used but not both.")


def run_http_client(args):
    # Help flag is turned on
    if args.help:
        if args.command == 'get':
            print(help_get)
        elif args.command == 'post':
            print(help_post)
        else:
            print(help_general)
    else:
        parsed_URL = urlparse(args.URL)
        host = parsed_URL.netloc
        path = parsed_URL.path if len(parsed_URL.path) > 0 else "/"
        query = parsed_URL.query

        # Connect to host
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, 80))

        if args.command == 'get':
            # Build the GET request
            request = "GET " + path

            # Append query params
            if len(query) > 0:
                request = request + "?" + query

            # Append host
            request = request + " HTTP/1.0\r\nHost:" + host + "\r\n"

            # Append headers
            if args.headers:
                for header in args.headers:
                    request = request + header + "\r\n"

            request = request + "\r\n"
            request_encoded = request.encode("utf-8")
            sock.send(request_encoded)

            response_encoded = sock.recv(1024)
            response = response_encoded.decode("utf-8")
            if args.verbose:
                print(response)
            else:
                # Remove details from the response if not verbose
                print(response.split("\r\n\r\n")[1])

            sock.close()
        elif args.command == 'post':
            # Build the POST request
            request = "POST " + path

            # Append query params
            if len(query) > 0:
                request = request + "?" + query

            # Append host
            request = request + " HTTP/1.0\r\nHost:" + host + "\r\n"

            # Append headers
            if args.headers:
                for header in args.headers:
                    request = request + header + "\r\n"

            # Append inline data
            if args.data:
                request = request + "Content-Length:" + str(len(args.data)) + "\r\n\r\n" + args.data

            # Append file data
            if args.file:
                file = open(args.file, "r")
                try:
                    file_content = file.read()
                    request = request + "Content-Length:" + str(len(file_content)) + "\r\n\r\n" + file_content
                except Exception as e:
                    print(f"An error has occured when reading the file:{e}")
                finally:
                    file.close()

            request = request + "\r\n"
            request_encoded = request.encode("utf-8")
            sock.send(request_encoded)

            response_encoded = sock.recv(1024)
            response = response_encoded.decode("utf-8")
            if args.verbose:
                print("VERBOSE")
                print(response)
            else:
                # Remove details from the response if not verbose
                print("NOT VERBOSE")
                print(response.split("\r\n\r\n")[1])

            sock.close()


# testrun()
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('--help', dest='help', action='store_true')
parser.add_argument('command', choices=['get', 'post', ''], nargs='?', default='')
parser.add_argument('-v', dest='verbose', action='store_true')
parser.add_argument('-h', dest='headers', action='append')
parser.add_argument('-d', dest='data')
parser.add_argument('-f', dest='file')
parser.add_argument('URL', action='store', nargs='?')
run_http_client(parser.parse_args())

# print(parser.parse_args(['get', '-h', 'someheader', "http://httpbin.org/get?course=networking&assignment=1"]))
# print(parser.parse_args())
