class Node():
	"""Class for a node of doubly linked list"""
	def __init__(self, key_id=None, key_val=None, prev_node=None, next_node=None):
		self.key_id = key_id
		self.key_val = key_val
		self.prev = prev_node
		self.next = next_node
