from pyDocStr import to_document, create_docstrings_from_file
from pyDocStr.utils import Formatter
from inspect import _empty


def test_decorator():
	def addition(a: int, b: int) -> int:
		return a + b

	class MyClass:
		def __init__(self):
			pass

		def method(self):
			pass


	print(type(addition))
	print(addition(3, 3))
	print(addition.description)
	print(addition.parameters)
	print(addition.returns)

	print(type(MyClass))


def test_formatter():
	formatter = Formatter.numpy_format()
	docstring = formatter.format_docstring(nb_base_tab=1, description="Une description", parameters={'a': (int, _empty), 'b': (int, _empty)}, returns={})
	print(docstring)


def functions_test():
	create_docstrings_from_file("./module_to_document.py", new_path="./module_documented.py")

def function_test2(module):
	create_docstrings_from_file(module, new_path="./module_documented.py")

if __name__ == "__main__":
	import module_to_document
	function_test2(module_to_document)
