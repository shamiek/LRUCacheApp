# Project Title and Description

Least Recently Used cache implemented with double linked list and a hashtable.
Actions into the cache - get and put have been externalized as a service exposed by REST API.
Default capacity of cache is 2.
Global variables are used to preserve cache state between requests to the app.

### Prerequisites

Python3

## Running the app

App usage: LRU_app.py [-h] [-c [CAPACITY]]

To fire up the app in a terminal on the default port 5000:

```
python LRU_app.py
```

For help

```
python LRU_app.py -h
```

### Testing the app

From another terminal use curl to test the app.

To put a key value pair to cache.

```
curl -X PUT http://127.0.0.1:5000/api/v1/put/4 -d "value=1600"
```

To get a key value pair from cache.

```
curl -X GET http://127.0.0.1:5000/api/v1/get/4
```

## Deployment

requirements.txt can be used for installing dependencies while deploying.

## Built With

* [Flask](http://flask.pocoo.org/) - a microframework for Python based on Werkzeug, Jinja 2 and good intentions.

## Authors

* **Shamiek** - [shamiek](https://github.com/shamiek)

## Acknowledgments

* Stackoverflow
* Python docs