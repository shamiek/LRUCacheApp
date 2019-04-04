from flask import Flask, request, abort, jsonify
from flask.views import MethodView
from node import Node
import logging
import argparse

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

app.config.from_pyfile('myconfig.cfg')

# cache data structures to be preserved through requests
keys_in_cache = {}
curr_cache_size = 0
dummy_head = Node()
dummy_tail = Node()
dummy_head.next = dummy_tail
dummy_tail.prev = dummy_head

class LRU(MethodView):
    """Implementation of LRU cache with doubly linked list and hashtable"""
    def __init__(self, capacity=2):
        self.cache_cap = capacity

    def move_to_front(self, node):
        """Moves node from current position to behind the dummy head"""
        self.snip_node_from_q(node)
        self.make_new_head(node)

    def snip_node_from_q(self, node):
        """Connects the node's successor and predecessor"""
        node.prev.next = node.next
        node.next.prev = node.prev

    def make_new_head(self, node):
        """Inserts node behind dummy_head"""
        node.next = dummy_head.next
        node.prev = dummy_head
        # reset dummy_head's successor node's predecessor
        # global dummy_head
        dummy_head.next.prev = node
        dummy_head.next = node

    def get(self, query_key_id):
        """Implements the get request response"""
        query_key_id = int(query_key_id)
        logging.debug('In get: len of dict: {}'.format(len(keys_in_cache)))
        self.print_dict()
        if query_key_id in keys_in_cache:
            node_to_move = keys_in_cache[query_key_id]
            self.move_to_front(node_to_move)
            return self.create_response(node=node_to_move)
        else:
            return str(404) + '\n'

    def evict_from_cache(self):
        """Evicts earliest used key from cache"""
        logging.info('Evicting from cache\n')
        node_to_evict = dummy_tail.prev
        del keys_in_cache[node_to_evict.key_id]
        self.snip_node_from_q(node_to_evict)
        global curr_cache_size
        curr_cache_size -= 1
        return node_to_evict

    def create_response(self, node=None):
        """Wrapper to create a response"""
        if node is None:
            response = jsonify()
        else:
            response = jsonify(key=node.key_id, value=node.key_val)
        response.status_code = 200
        return response

    def print_dict(self):
        """Prints the hashtable containing keys in cache. Useful for debugging"""
        logging.debug('[print_dict]: len of dict: {}'.format(len(keys_in_cache)))
        for k in keys_in_cache:
            logging.debug('[print_dict]: {}:{}'.format(k, keys_in_cache[k].key_val))

    def put(self, key_id):
        """Implements the put request response"""
        key_id = int(key_id)
        value_str = request.get_data().decode(encoding='UTF-8')
        #Extract value for key_id
        key_val = int(value_str.split('=')[1])
        if key_id not in keys_in_cache:
            logging.debug('[put]: String {} value in string: {} \n'.format(value_str, value_str.split('=')[1]))
            new_node = Node(key_id=int(key_id), key_val=key_val)
            self.print_dict()
            keys_in_cache[key_id] = new_node
            self.print_dict()
            self.make_new_head(new_node)
            global curr_cache_size
            logging.debug('[Before increment]: curr_cache_size: {}, cache_capacity: {}'.format(curr_cache_size, self.cache_cap))
            curr_cache_size += 1
            logging.debug('[After increment]: curr_cache_size: {}, cache_capacity: {}'.format(curr_cache_size, self.cache_cap))
            #Evict key if cache size exceeded due to current insertion
            if curr_cache_size > self.cache_cap:
                evicted_node = self.evict_from_cache()
                return self.create_response(node=evicted_node)
            else:
                return self.create_response()    
        else:
            # update value for this key
            keys_in_cache[key_id].key_val = key_val
            self.move_to_front(keys_in_cache[key_id])
            return self.create_response()

func_view_of_class = LRU.as_view('func_view')
app.add_url_rule('/api/v1/get/', methods = ['GET'], view_func=func_view_of_class)
app.add_url_rule('/api/v1/get/<query_key_id>', methods = ['GET'], view_func=func_view_of_class)
app.add_url_rule('/api/v1/put/<key_id>', methods = ['PUT'], view_func=func_view_of_class)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='An LRU cache with actions get and put externalized as service')
    parser.add_argument('-c', '--capacity', type=int, nargs='?', const=2, help='Capacity of the cache')
    args = parser.parse_args()
    lru_cache = LRU(capacity=args.capacity)
    app.run()
