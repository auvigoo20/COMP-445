import argparse
from urllib.parse import urlparse
from httpc_library import build_http_request, send_request

help_general = ("httpc is a curl-like application but supports HTTP protocol only.\n"
                "Usage:\n"
                "httpc command [arguments]\n"
                "The commands are:\n"
                "\tget executes a HTTP GET request and prints the response.\n"
                "\tpost executes a HTTP POST request and prints the response.\n"
                "\thelp prints this screen.\n"
                "Use \"httpc --help [command]\" for more information about a command.\n")

help_get = ("usage: httpc get [-v] [-h key:value] [-r] [-o output-file] URL\n"
            "Get executes a HTTP GET request for a given URL.\n"
            "\t-v Prints the detail of the response such as protocol, status, and headers.\n"
            "\t-h key:value Associates headers to HTTP Request with the format 'key:value'.\n"
            "\t-r Allows redirection to occur when responses have status codes 3xx.\n"
            "\t-o output-file Write the console output to an external file.\n")

help_post = ("usage: httpc post [-v] [-h key:value] [-d inline-data] [-f file] URL\n"
             "Post executes a HTTP POST request for a given URL with inline data or from file.\n"
             "\t-v Prints the detail of the response such as protocol, status, and headers.\n"
             "\t-h key:value Associates headers to HTTP Request with the format 'key:value'.\n"
             "\t-d string Associates an inline data to the body HTTP POST request.\n"
             "\t-f file Associates the content of a file to the body HTTP POST request.\n"
             "\t-r Allows redirection to occur when responses have status codes 3xx.\n"
             "\t-o output-file Write the console output to an external file.\n"
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
        if len(host) < 1:
            host = "localhost"
        request = build_http_request(args.URL, args.command, args.headers, args.data, args.file)
        response = send_request(host, request, 8080)

        # REDIRECTION HANDLING (response codes 3xx)
        if args.redirect:
            response_details = response.split("\r\n\r\n")[0]
            response_status_line = response_details.split("\n")[0]
            response_code = response_status_line.split(" ")[1]  # Get response code
            while response_code[0] == "3":
                response_lines = response_details.split("\r\n")
                redirect_url = ""

                # Get redirection URL
                for line in response_lines:
                    if "Location:" in line:
                        redirect_url = line.split(" ")[1]

                print("REDIRECTION " + response_code + " TO: " + redirect_url)
                if "http:" not in redirect_url and "https:" not in redirect_url:
                    # Build the whole URL if it's a relative redirect
                    redirect_url = parsed_URL.scheme + "://" + host + redirect_url
                args.URL = redirect_url
                # Send new request
                request = build_http_request(args.URL, args.command, args.headers, args.data, args.file)
                response = send_request(host, request, 8007)

                # Check the status code of the newly sent request. If it is 3xx, repeat the process again
                response_details = response.split("\r\n\r\n")[0]
                response_status_line = response_details.split("\n")[0]
                response_code = response_status_line.split(" ")[1]

        if not args.verbose:
            response = response.split("\r\n\r\n")[1]    # Remove the response details if not verbose
        if args.output_file:
            file = open(args.output_file, "w")
            try:
                file.write(response)
            except Exception as e:
                print(f"An error has occured when writing to the file:{e}")
            finally:
                file.close()
        else:
            print(response)


parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('--help', dest='help', action='store_true')
parser.add_argument('command', choices=['get', 'post', ''], nargs='?', default='')
parser.add_argument('-v', dest='verbose', action='store_true')
parser.add_argument('-h', dest='headers', action='append')
parser.add_argument('-d', dest='data')
parser.add_argument('-f', dest='file')
parser.add_argument('-r', dest='redirect', action='store_true')
parser.add_argument('URL', action='store', nargs='?')
parser.add_argument('-o', dest='output_file')
run_http_client(parser.parse_intermixed_args())
