# COMP 445 Lab Assignment #1

Written by: Auvigoo Ahmed (40128901)

To test this out, you could use the following commands:

## ASSIGNMENT 1 TEST INPUTS

HELP REQUESTS:
- ``python httpc.py --help``
- ``python httpc.py --help get``
- ``python httpc.py --help post``

GET REQUESTS:
- ``python httpc.py get 'http://httpbin.org/get?course=networking&assignment=1' -v``
- ``python httpc.py get 'http://httpbin.org/absolute-redirect/3' -v -r``
- ``python httpc.py get 'http://httpbin.org/redirect/3' -v -r``

POST REQUESTS:
- ``python httpc.py post -h Content-Type:application/json -d '{\"Assignment\": 1}' http://httpbin.org/post -v``
- ``python httpc.py post -h Content-Type:application/json -f input.txt http://httpbin.org/post -v``


## ASSIGNMENT 2 TEST INPUTS

First, start the httpfs server by running:
`python httpfs.py`

If you want to run it in port 9090 and directory `/testfolder`, run this command:

`python httpfs.py -p 9090 -d '/testfolder''`

In a separate terminal, run the `httpc` client, for example:

`python httpc.py get 'http://localhost:8080/testfolder/abc.txt' -v`

`python httpc.py post 'http://localhost:8080/testfolder/newfile.txt' -d 'Some data to insert into a new file' -v`
