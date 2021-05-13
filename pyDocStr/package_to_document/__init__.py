import email
from . import subpackage1
from .subpackage2 import module3
from . import module1

from pyDocStr import to_document


@to_document(description="A function")
def function_init(a: int, b: float):
	print(a, b)