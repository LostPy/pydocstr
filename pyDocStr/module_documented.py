from pyDocStr import to_document
from typing import List, Tuple


class UneClasse:
	"""Une classe random
	
	Attributes
	
		method1 : {TYPE}
			{DESCRIPTION}
		one : {TYPE}
			{DESCRIPTION}
		three : {TYPE}
			{DESCRIPTION}
		two : {TYPE}
			{DESCRIPTION}
	
	Public methods
	
		method1 : {TYPE}
			{DESCRIPTION}
	
	Protected methods
	
	None
	"""
	one = 1
	two = 2
	three = 3

	def method1(self, arg1: int = 3):
		"""Une méthode random
		
		Parameters
		
			OPTIONNAL[arg1] : int
				{DESCRIPTION}
				Default: 3
		
		Returns
		
		None
		"""
		print(arg1)


def additions(a: int, b: int) -> int:
	"""Une fonction pour addionner deux nombres.
	
	Parameters
	
		a : int
			{DESCRIPTION}
		b : int
			{DESCRIPTION}
	
	Returns
	
		result : int
			{DESCRIPTION}
	"""
	return a + b


def somme(list_: List[int]) -> int:
	"""Une fonction qui somme une liste.
	
	Parameters
	
		list_ : List[int]
			{DESCRIPTION}
	
	Returns
	
		result : int
			{DESCRIPTION}
	"""
	return sum(list_)


def get_positions() -> Tuple[int, int]:
	"""Une fonction sans arguments.
	
	Parameters
	
	None
	
	Returns
	
		result : Tuple[int, int]
			{DESCRIPTION}
	"""
	return 3, 4


def default_args_example(a, b=3, c: str = "Hello World"):
	"""Une fonction avec des arguments ayant une valeur par défaults.
	
	Parameters
	
		a : {TYPE}
			{DESCRIPTION}
		OPTIONNAL[b] : {TYPE}
			{DESCRIPTION}
			Default: 3
		OPTIONNAL[c] : str
			{DESCRIPTION}
			Default: Hello World
	
	Returns
	
	None
	"""
	print(a, b, c)


def other_function_to_document():
	"""Une fonction sans typage ni argument.
	
	Parameters
	
	None
	
	Returns
	
	None
	"""
	def a_function_in_function():
		pass


def function_with_multi_lines(a, b, c, d, e, f, g: int, h: str,
								i: float, j: float, k: tuple,
								l: int = 3, m: int = 2):
	"""Une fonction définie sur plusieurs lignes.
	
	Parameters
	
		a : {TYPE}
			{DESCRIPTION}
		b : {TYPE}
			{DESCRIPTION}
		c : {TYPE}
			{DESCRIPTION}
		d : {TYPE}
			{DESCRIPTION}
		e : {TYPE}
			{DESCRIPTION}
		f : {TYPE}
			{DESCRIPTION}
		g : int
			{DESCRIPTION}
		h : str
			{DESCRIPTION}
		i : float
			{DESCRIPTION}
		j : float
			{DESCRIPTION}
		k : tuple
			{DESCRIPTION}
		OPTIONNAL[l] : int
			{DESCRIPTION}
			Default: 3
		OPTIONNAL[m] : int
			{DESCRIPTION}
			Default: 2
	
	Returns
	
	None
	"""
	pass

def other_function(a, b):
	print(a, b)
