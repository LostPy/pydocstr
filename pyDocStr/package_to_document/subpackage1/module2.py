from pyDocStr import to_document

@to_document(description="a function to print one or several 'random'")
def print_random(nb: int) -> str:
	return "random "*nb