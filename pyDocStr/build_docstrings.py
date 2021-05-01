"""Module to generate Functions documentation string."""
import os
from inspect import getsource, getmembers, isfunction, signature, _empty
import re


from .documented import FunctionToDocument, ClassToDocument, to_document
from .utils import Formatter, load_module
from . import _logger


@to_document(description="A function to get the start and end position of a function")
def get_function_positions(func_name: str, source_code: str) -> tuple:
	_logger.debug(f"get the function positions of '{func_name}'...")
	r = r'def\s+{name}\s*\(.*?\)\s*[-, >]*[a-z, A-Z, \[, \], \,]*\:'.format(name=func_name)
	result = re.search(r, source_code, re.MULTILINE | re.DOTALL)
	_logger.debug(f"list result for '{func_name}': {re.findall(r, source_code)}")
	return result.span()


@to_document(description="A function to get the start and end position of a class")
def get_class_positions(class_name: str, source_code: str) -> tuple:
	_logger.debug(f"get the class positions of '{class_name}'...")
	r = r'class\s+{name}.*?\s*:'.format(name=class_name)
	return re.search(r, source_code, re.MULTILINE | re.DOTALL).span()


def get_docstring_start(end_signature: int, source_code: str) -> int:
	return source_code.find('\n', end_signature) + 1


@to_document(description="Add the docstring in the text of source file.")
def write_docstring(docstring: str, source_code: str, start: int) -> str:
	_logger.debug(f"Add a docstring to the source code...")
	source_code = source_code[:start] + docstring + source_code[start:]
	return source_code


@to_document(description="A function to build the docstring of a functi")
def build_function_docstring(func_to_doc: FunctionToDocument, formatter: Formatter) -> str:
	_logger.debug(f"Build function docstring for '{func_to_doc.name}'...")
	return formatter.format_docstring(nb_base_tab=func_to_doc.nb_base_tab,
										description=func_to_doc.description,
										fields={
													'Parameters': func_to_doc.parameters,
													'Returns': func_to_doc.returns
												})


@to_document(description="A function to build the docstring of a class")
def build_class_docstring(class_to_doc: ClassToDocument, formatter: Formatter) -> str:
	_logger.debug(f"Build class docstring for '{class_to_doc.name}'...")
	return formatter.format_docstring(nb_base_tab=class_to_doc.nb_base_tab,
										description=class_to_doc.description,
										fields={
													'Attributes': class_to_doc.attributes,
													'Public methods': class_to_doc.public_methods,
													'Protected methods': class_to_doc.protected_methods,
												})


@to_document(description="Function to remove all 'to_document' decorator")
def _remove_decorators(source_code: str, decorator_name: str = "to_document") -> str:
	_logger.info(f"Removing decorators '{decorator_name}'...")
	r = r"\t*?@{decorator_name}\(.*?\).*?\n".format(decorator_name=decorator_name)
	return re.sub(r, "", source_code)


def create_functions_docstrings(list_functions: list, source_code: str, formatter: Formatter) -> str:
	_logger.info("Create functions docstrings...")
	for func in list_functions:
		_logger.debug(f"Create function docstring of {func.name}")
		docstring = build_function_docstring(func, formatter)
		pos = get_function_positions(func.name, source_code)
		source_code = write_docstring(docstring, source_code, get_docstring_start(pos[1], source_code))
	return source_code


def create_class_docstrings(list_class: list, source_code: str, formatter: Formatter):
	_logger.info("Create class docstrings...")
	for class_ in list_class:
		_logger.debug(f"Create class docstring of {class_.name}")
		docstring = build_class_docstring(class_, formatter)
		pos = get_class_positions(class_.name, source_code)
		source_code = write_docstring(docstring, source_code, get_docstring_start(pos[1], source_code))
		source_code = create_functions_docstrings(class_.methods_to_document, source_code, formatter)
	return source_code


def _get_members_to_document(module):
	_logger.info(f"Get all functions and class to documented from module `{module.__name__}`")
	list_func, list_class = [], []
	for member in getmembers(module):
		if isinstance(member[1], FunctionToDocument):
			list_func.append(member[1])
		elif isinstance(member[1], ClassToDocument):
			list_class.append(member[1])
	_logger.debug(f"list_func = {list_func}")
	_logger.debug(f"list_class = {list_class}")
	return list_func, list_class


@to_document(description="Create all docstrings of functions and class decorated with 'to_document' decorator for a file.")
def create_docstrings_from_file(path: str, formatter: Formatter = Formatter.simple_format(), new_path: str = None,
								remove_decorator: bool = True, decorator_name: str = 'to_document'):
	_logger.info(f"Start to document the file '{path}'")
	_logger.info(f"Import module from path: '{path}'...")
	try:
		module = load_module._import_from_path(path)
	except (ImportError, ModuleNotFoundError):	
		logger.error(f"The module from '{path}', was not founded")
		return

	list_func, list_class = _get_members_to_document(module)

	_logger.info("Get source code...")
	source_code = getsource(module)

	new_source_code = create_functions_docstrings(list_func, source_code, formatter)
	new_source_code = create_class_docstrings(list_class, new_source_code, formatter)
	if remove_decorator:
		new_source_code = _remove_decorators(new_source_code, decorator_name=decorator_name)

	new_path = path if new_path is None else new_path
	_logger.info(f"Write the new source code with docstring in '{new_path}'...")
	with open(new_path, 'w') as f:
		f.write(new_source_code)
	_logger.info(f"The file '{path}' was documented with success.")


@to_document(description="Create docstrings for all python files in a folder, for functions and class decorated with 'to_document' decorator.")
def create_docstrings_from_folder(folderpath: str, formatter: Formatter = Formatter.simple_format(), new_folderpath: str = None,
									subfolders: bool = False, remove_decorator: bool = True, decorator_name: str = 'to_document'):
	_logger.info(f"Start to document the folder: {folderpath}")
	_logger.info(f"Document subfolders: {subfolders}")
	for elmt in os.listdir(folderpath):
		path_elmt = os.path.join(folderpath, elmt)
		if new_folderpath is not None:
			if not os.path.exists(new_folderpath):
				os.mkdir(new_folderpath)
			new_path_elmt = os.path.join(new_folderpath, elmt)
		else:
			new_path_elmt = None

		if os.path.isfile(elmt) and elmt[-3:] == '.py':
			create_docstrings_from_file(path_elmt, formatter,
										new_path=new_path_elmt,
										remove_decorator=remove_decorator,
										decorator_name=decorator_name)
		elif os.path.isdir(elmt):
			create_docstrings_from_folder(path_elmt, formatter, new_path_elmt, subfolders, remove_decorator, decorator_name)

