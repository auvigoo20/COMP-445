# COMP 445 Lab Assignment #1

Written by: Auvigoo Ahmed (40128901)

To test this out, you could use the following commands:

GET REQUESTS:
- ``python httpc.py get 'http://httpbin.org/get?course=networking&assignment=1' -v``
- ``python httpc.py get 'http://httpbin.org/absolute-redirect/3' -v -r``
- ``python httpc.py get 'http://httpbin.org/redirect/3' -v -r``

POST REQUESTS:
- ``python httpc.py post -h Content-Type:application/json -d '{\"Assignment\": 1}' http://httpbin.org/post -v``
- ``python httpc.py post -h Content-Type:application/json -f input.txt http://httpbin.org/post -v``

