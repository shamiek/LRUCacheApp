LRU_app.py implements a Least Recently used cache with double linked list and a hashtable.
Actions into the cache - get and put have been externalized as a service exposed by REST API.
Flask module has been used to implement the REST API.
Default capacity of cache is 2.
Global variables are used to preserve cache state between requests to the app.

To fire up the app on default port 5000:

usage: LRU_app.py [-h] [-c [CAPACITY]]

Test app from another terminal using curl:

To put a value:
$ curl -X PUT http://127.0.0.1:5000/api/v1/put/4 -d "value=1600"

To get a value:
$ curl -X GET http://127.0.0.1:5000/api/v1/get/4

Deployment:
requirements.txt can be used for installing dependencies while deploying.