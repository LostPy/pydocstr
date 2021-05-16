from pyDocStr import to_document


@to_document(description="a function")
def function1(a: int, b: int) -> int:
	return a + b