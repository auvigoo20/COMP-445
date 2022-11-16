import datetime
import os

http_version = 'HTTP/1.0'


def build_response_from_request(request, server_directory, debug_messages):
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

    debug_message_to_print = ''

    if request_method == 'GET':
        debug_message_to_print += 'Building GET response...\n'
        # Prevent the user from accessing files outside the working directory (for example Assignment2/testfolder/../..)
        request_url_absolute_path = os.path.abspath(server_directory + request_url)
        debug_message_to_print += 'Requested URL absolute path: ' + request_url_absolute_path + '\n'
        if not request_url_absolute_path.startswith(server_directory):
            debug_message_to_print += 'Requested URL path is outside of the working directory...\n'
            response_code = '403 Forbidden'
        else:  # Check if path is invalid, a file or a directory
            if not os.path.exists(request_url_absolute_path):
                debug_message_to_print += 'Requested URL path does not exist\n'
                response_code = '404 Not Found'

            # GET /dir
            elif os.path.isdir(request_url_absolute_path):
                debug_message_to_print += 'Requested path is a directory\n'
                try:
                    list_of_files = os.listdir(request_url_absolute_path)
                    for i in list_of_files:
                        response_body = response_body + i + '\r\n'
                    response_code = '200 OK'
                except IOError:
                    response_code = '400 Bad request'

            # GET /foo.x
            elif os.path.isfile(request_url_absolute_path):
                debug_message_to_print += 'Requested path is a file\n'
                try:
                    file_to_read = open(request_url_absolute_path)
                    response_body = response_body + file_to_read.read()
                    response_code = '200 OK'
                    file_to_read.close()
                    debug_message_to_print += 'File has been read successfully\n'
                except IOError:
                    debug_message_to_print += 'Requested URL file path does not exist\n'
                    response_code = '404 Not Found'
    elif request_method == 'POST':
        debug_message_to_print += 'Building POST response...\n'
        # Prevent the user from accessing files outside the working directory (for example
        # Assignment2/testfolder/../..)
        request_url_absolute_path = os.path.abspath(server_directory + request_url)
        debug_message_to_print += 'Requested URL absolute path: ' + request_url_absolute_path + '\n'
        if not request_url_absolute_path.startswith(server_directory):
            debug_message_to_print += 'Requested URL path is outside of the working directory...\n'
            response_code = '403 Forbidden'
        else:
            try:
                file_to_write = open(request_url_absolute_path, 'w')
                file_to_write.write(request_body)
                response_code = '201 Created'
                file_to_write.close()
                debug_message_to_print += 'File has been created successfully\n'
            except IOError:
                debug_message_to_print += 'Requested URL path does not exist\n'
                response_code = '404 Not Found'

    if debug_messages:
        print(debug_message_to_print)

    now = datetime.datetime.now(datetime.timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')
    response_header = response_header + http_version + ' ' + response_code + '\r\nDate: ' + now
    response_header = response_header + '\r\nContent-Type: text\r\nContent-Length: ' + str(
        len(response_body)) + '\r\nConnection: close\r\nServer: httpfs\r\n\r\n'

    final_response = response_header + response_body
    return final_response
