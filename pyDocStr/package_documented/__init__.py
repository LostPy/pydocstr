import email
from . import subpackage1
from .subpackage2 import module3
from . import module1

from pyDocStr import to_document


def function_init(a: int, b: float):
	"""A function
	
	Parameters
	
	a : int
		{DESCRIPTION}
	b : float
		{DESCRIPTION}
	
	Returns
	
	None
	"""
	print(a, b)
