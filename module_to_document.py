from pyDocStr import to_document
from typing import List, Tuple


@to_document(description="Une class random")
class UneClasse:
	one = 1
	two = 2
	three = 3

	@to_document(description="Une méthode random")
	def method1(self, arg1: int = 3):
		print(arg1)


@to_document(description="Une fonction pour additioner deux nombres.")
def additions(a: int, b: int) -> int:
	return a + b


@to_document(description="Une fonction pour réaliser la somme d'une liste.")
def somme(list_: List[int]) -> int:
	return sum(list_)


@to_document(description="Une fonction qui donne la positions d'un point")
def get_positions() -> Tuple[int, int]:
	return 3, 4


@to_document(description="Une fonction avec des arguments non typé et avec une valeurs par défault")
def default_args_example(a, b=3, c: str = "Hello World"):
	print(a, b, c)


@to_document()
def other_function_to_document():
	@to_document()
	def a_function_in_function():
		pass

@to_document(description="Fonction définie sur plusieurs lignes")
def function_with_multi_lines(a, b, c, d, e, f, g: int, h: str,
								i: float, j: float, k: tuple,
								l: int = 3, m: int = 2):
	pass

def other_function(a, b):
	print(a, b)