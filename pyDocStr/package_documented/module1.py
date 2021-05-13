
from pyDocStr import to_document

from . import module3


def hello_world():
	"""a function hello world
	
	Parameters
	
	None
	
	Returns
	
	None
	"""
	print("Hello world")


def write_message(msg: str):
	"""a function to print a message
	
	Parameters
	
	msg : str
		{DESCRIPTION}
	
	Returns
	
	None
	"""
	print(msg)
