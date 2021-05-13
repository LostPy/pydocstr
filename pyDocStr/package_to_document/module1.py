
from pyDocStr import to_document

from . import module3


@to_document(description="a function hello world")
def hello_world():
	print("Hello world")


@to_document(description="a function to print a message")
def write_message(msg: str):
	print(msg)