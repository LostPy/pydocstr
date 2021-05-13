import re
from .module2 import print_random

from pyDocStr import to_document


@to_document(description="a function to return a empty list")
def empty_list() -> list:
	return []