from pyDocStr import to_document


@to_document(description="a function")
def function2(a: int, b: int) -> int:
	return a - b