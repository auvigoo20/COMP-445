import argparse
import socket


def testrun():

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "google.ca"

    sock.connect((host, 80))

    # GET only
    line = "GET /?q=hello+world HTTP/1.0\r\nHost:google.ca\r\n\r\n"

    # GET with query params
    # line = "GET /get?course=networking&assignment=1 HTTP/1.0\r\nHost:httpbin.org\r\n\r\n"

    # POST with header and inline data
    # someJSON = "{\"Assignment\":1}"
    # line = "POST /post HTTP/1.0\r\nHost:httpbin.org\r\nContent-Type:application/json\r\n" + "Content-Length:" + str(len(someJSON)) + "\r\n\r\n" + someJSON + "\r\n"

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


# def run_http_client(method, verbose, headers, data, file, URL):

# testrun()
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('--help', action='store_true')
parser.add_argument('command', choices=['get', 'post', ''], nargs='?', default='')
parser.add_argument("-v", action="store_true")
parser.add_argument("-h", action="append", nargs="*")
parser.add_argument('-d')
parser.add_argument('-f')
parser.add_argument("URL",  nargs='?')
args = parser.parse_args()
print(args)
