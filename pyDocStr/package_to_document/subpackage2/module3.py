import os
from pyDocStr import to_document


@to_document(description="a function addition")
def addition(a: int, b: int) -> int:
	return a + b


@to_document(description="a function product")
def product(a: int, b: int) -> int:
	return a * b