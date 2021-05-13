"""Module to generate Functions documentation string."""
import os
import traceback
from inspect import getsource, getmembers, isfunction, signature, _empty, ismodule
from distutils.dir_util import copy_tree, DistutilsFileError
import re

from .documented import FunctionToDocument, ClassToDocument
from .utils import Formatter, _modules_utils
from . import _logger


def get_function_positions(func_name: str, source_code: str) -> tuple:
	"""A function to get the start and end position of a function
	
	Parameters
	----------
	func_name : str
		The function name
	source_code : str
		The source code
	
	Returns
	-------
	pos : tuple
		The start and end positions of the class
	"""
	_logger.debug(f"get the function positions of '{func_name}'...")
	r = r'def\s+{name}\s*\(.*?\)\s*[-, >]*[a-z, A-Z, \[, \], \,]*\:'.format(name=func_name)
	result = re.search(r, source_code, re.MULTILINE | re.DOTALL)
	_logger.debug(f"list result for '{func_name}': {re.findall(r, source_code)}")
	return result.span()


def get_class_positions(class_name: str, source_code: str) -> tuple:
	"""A function to get the start and end position of a class
	
	Parameters
	----------
	class_name : str
		The class name
	source_code : str
		The source code
	
	Returns
	-------
	pos : tuple
		The start and end positions of the class
	"""
	_logger.debug(f"get the class positions of '{class_name}'...")
	r = r'class\s+{name}.*?\s*:'.format(name=class_name)
	return re.search(r, source_code, re.MULTILINE | re.DOTALL).span()


def get_docstring_start(end_signature: int, source_code: str) -> int:
	"""A function to get the start position of a docstring
	
	Parameters
	----------
	end_signature : int
		The end position of the signature of function
	source_code : str
		The source code
	
	Returns
	-------
	result : int
		The start position of docstring
	"""
	return source_code.find('\n', end_signature) + 1


def write_docstring(docstring: str, source_code: str, start: int) -> str:
	"""Add the docstring in the text of source file.
	
	Parameters
	----------
	docstring : str
		The docstring to insert
	source_code : str
		The source code where add the docstring
	start : int
		The start position of docstring
	
	Returns
	-------
	source_code : str
		The new source code with docstring
	"""
	_logger.debug(f"Add a docstring to the source code...")
	source_code = source_code[:start] + docstring + source_code[start:]
	return source_code


def build_function_docstring(func_to_doc: FunctionToDocument, formatter: Formatter) -> str:
	"""A function to build the docstring of a functi
	
	Parameters
	----------
	func_to_doc : FunctionToDocument
		The function to document
	formatter : Formatter
		The formatter to use
	
	Returns
	-------
	docstring : str
		The docstring for this function
	"""
	_logger.debug(f"Build function docstring for '{func_to_doc.name}'...")
	return formatter.format_docstring(nb_base_tab=func_to_doc.nb_base_tab,
										description=func_to_doc.description,
										fields={
													'Parameters': func_to_doc.parameters,
													'Returns': func_to_doc.returns
												})


def build_class_docstring(class_to_doc: ClassToDocument, formatter: Formatter) -> str:
	"""A function to build the docstring of a class
	
	Parameters
	----------
	class_to_doc : ClassToDocument
		The class to document
	formatter : Formatter
		The formatter to use
	
	Returns
	-------
	docstring : str
		The docstring for this class
	"""
	_logger.debug(f"Build class docstring for '{class_to_doc.name}'...")
	return formatter.format_docstring(nb_base_tab=class_to_doc.nb_base_tab,
										description=class_to_doc.description,
										fields={
													'Attributes': class_to_doc.attributes,
													'Public methods': class_to_doc.public_methods,
													'Protected methods': class_to_doc.protected_methods,
												})


def _remove_decorators(source_code: str, decorator_name: str = "to_document") -> str:
	"""Function to remove all 'to_document' decorator
	
	Parameters
	----------
	source_code : str
		The source code
	OPTIONAL[decorator_name] : str
		The name of decorator to remove
		Default: "to_document"
	
	Returns
	-------
	source_code : str
		The new source code without decorator 'decorator_name'
	"""
	_logger.info(f"Removing decorators '{decorator_name}'...")
	r = r"\t*?@{decorator_name}\(.*?\).*?\n".format(decorator_name=decorator_name)
	return re.sub(r, "", source_code)


def create_functions_docstrings(list_functions: list, source_code: str, formatter: Formatter) -> str:
	"""A function to create docstring for all functions of a list.
	
	Parameters
	----------
	list_functions : list
		The list of functions to document
	source_code : str
		The source code
	formatter : Formatter
		The formatter to use
	
	Returns
	-------
	source_code : str
		The new source code with docstrings
	"""
	_logger.info("Create functions docstrings...")
	for func in list_functions:
		_logger.debug(f"Create function docstring of {func.name}")
		docstring = build_function_docstring(func, formatter)
		pos = get_function_positions(func.name, source_code)
		source_code = write_docstring(docstring, source_code, get_docstring_start(pos[1], source_code))
	return source_code


def create_class_docstrings(list_class: list, source_code: str, formatter: Formatter):
	"""A function to create docstring for all class of a list.
	
	Parameters
	----------
	list_class : list
		The list of class to document
	source_code : str
		The source code
	formatter : Formatter
		The formatter to use

	Returns
	-------
	source_code : str
		The source code with news docstrings
	"""
	_logger.info("Create class docstrings...")
	for class_ in list_class:
		_logger.debug(f"Create class docstring of {class_.name}")
		docstring = build_class_docstring(class_, formatter)
		pos = get_class_positions(class_.name, source_code)
		source_code = write_docstring(docstring, source_code, get_docstring_start(pos[1], source_code))
		source_code = create_functions_docstrings(class_.methods_to_document, source_code, formatter)
	return source_code


def _get_members_to_document(module):
	"""A function to get the list of functions and class to document.
	
	Parameters
	----------
	module : Module
		The module where get functions and class to document.
	
	Returns
	-------
	list_func  : List[FunctionToDocument]
		The list of functions to document
	list_class : List[ClassToDocument]
		The list of class to document
	"""
	_logger.info(f"Get all functions and class to documented from module `{module.__name__}`")
	list_func, list_class = [], []
	for member in getmembers(module):
		if isinstance(member[1], FunctionToDocument) and member[1].obj.__module__ == module.__name__:
			list_func.append(member[1])
		elif isinstance(member[1], ClassToDocument) and member[1].obj.__module__ == module.__name__:
			list_class.append(member[1])
	_logger.debug(f"list_func = {list_func}")
	_logger.debug(f"list_class = {list_class}")
	return list_func, list_class


#@to_document(description="A function to import a module and get this path.")
def _safe_import_module(path_or_module):
	if isinstance(path_or_module, str) and os.path.exists(path_or_module):
		_logger.info(f"Import module from path: '{path_or_module}'...")
		_logger.debug(f"path_or_module: {path_or_module}")
		try:
			return os.path.abspath(path_or_module), _modules_utils._import_from_path(path_or_module)
		except ImportError:	
			_logger.error(f"The module from path '{path_or_module}', was not founded or we can't import this module")
			_logger.debug(traceback.format_exc())
			return os.path.abspath(path_or_module), None
	elif isinstance(path_or_module, str):
		_logger.error(f"The path {path_or_module} was not found")
		return path_or_module, None

	elif ismodule(path_or_module):
		return os.path.abspath(path_or_module.__file__), path_or_module

	raise ValueError(f"'path_or_module' must be an instance of str or a module, not a {type(path_or_module)}")


def create_docstrings_from_module(path_or_module, formatter: Formatter = Formatter.simple_format(), new_path: str = None,
								remove_decorator: bool = True, decorator_name: str = 'to_document'):
	"""Create all docstrings of functions and class decorated with 'to_document' decorator for a file.
	
	Parameters
	----------
	path_or_module : Union[str, module]
		The path of python file to document or the module to document.
	OPTIONAL[formatter] : Formatter
		The formatter to use.
		Default: The 'simple' formatter. Get with `pyDocStr.utils.Formatter.simple_format()`
	OPTIONAL[new_path] : str
		The new python file path where the source code with docstrings must be saved. If None, the old file is overwritten.
		Default: None
	OPTIONAL[remove_decorator] : bool
		If True, decorators 'to_document' specify with 'decorator_name' argument are removed.
		Default: True
	OPTIONAL[decorator_name] : str
		The decorator name use for 'to_document'
		Default: to_document

	Returns
	-------
	None
	"""
	path, module = _safe_import_module(path_or_module)

	_logger.info(f"Start to document the module '{module.__name__}'")
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


def create_docstrings_from_folder(folderpath: str, formatter: Formatter = Formatter.simple_format(), new_folderpath: str = None,
									subfolders: bool = False, remove_decorator: bool = True, decorator_name: str = 'to_document'):
	"""Create docstrings for all python files in a folder, for functions and class decorated with 'to_document' decorator.
	
	Parameters
	----------
	folderpath : str
		The path of folder to document.
	OPTIONAL[formatter] : Formatter
		The formatter to use.
		Default: The 'simple' formatter. Get with `pyDocStr.utils.Formatter.simple_format()`
	OPTIONAL[new_folderpath] : str
		The path of folder where the news files must be save. If None, the files are overwritten
		Default: None
	OPTIONAL[subfolders] : bool
		If True, all files of subfolders are documented.
		Default: False
	OPTIONAL[remove_decorator] : bool
		If True, decorators 'to_document' specify with 'decorator_name' argument are removed.
		Default: True
	OPTIONAL[decorator_name] : str
		The decorator name use for 'to_document'
		Default: to_document

	Returns
	-------
	None
	"""
	_logger.info(f"Start to document the folder: {folderpath}")
	_logger.info(f"Document subfolders: {subfolders}")
	_logger.debug(f"List directories and file: {os.listdir(folderpath)}")
	for elmt in os.listdir(folderpath):
		path_elmt = os.path.join(folderpath, elmt)
		print(path_elmt, os.path.isfile(path_elmt), path_elmt[-3:] == '.py')
		if new_folderpath is not None:
			if not os.path.exists(new_folderpath):
				os.mkdir(new_folderpath)
			new_path_elmt = os.path.join(new_folderpath, elmt)
		else:
			new_path_elmt = None

		if os.path.isfile(path_elmt) and path_elmt[-3:] == '.py':
			create_docstrings_from_module(path_elmt, formatter,
										new_path=new_path_elmt,
										remove_decorator=remove_decorator,
										decorator_name=decorator_name)
		elif subfolders and os.path.isdir(path_elmt):
			create_docstrings_from_folder(path_elmt, formatter, new_path_elmt, subfolders, remove_decorator, decorator_name)


#@to_document(description="Create docstrings for all python files in a package, for functions and class decorated with 'to_document' decorator.")
def create_docstrings_from_package(path_or_package, formatter: Formatter = Formatter.simple_format(), new_package_path: str = None,
									subpackages: bool = False, remove_decorator: bool = True, decorator_name: str = 'to_document'):
	def new_path_module(module, package_path: str):
		# return the new path for a module
		if new_package_path is not None:
			module_path = os.path.abspath(module.__file__)
			print(module.__name__, module_path)
			base_path = os.path.commonpath([os.path.abspath(package_path), os.path.abspath(module.__file__)])
			relative_path = module_path[len(base_path):].strip("/") if base_path != module_path else './'
			if os.path.isdir(relative_path):  # if module is a package
				relative_path = os.path.join(relative_path, '__init__.py')
			return os.path.join(new_package_path, relative_path)
		return None

	if isinstance(path_or_package, str) and not os.path.exists(path_or_package):
		_logger.error((f"The file {path_or_package} wasn't found"))
		return

	new_package_path = os.path.abspath(new_package_path)  # safe new path

	path, package = _safe_import_module(path_or_package)
	if package is None:
		return

	_logger.info(f"Start to document the package: {package.__name__}")
	_logger.info(f"Document subpackages: {subpackages}")

	# get the list of modules (getmembers & ismodule) from package (dirname(package) == commonpath([package, module]))
	list_modules = [member for name, member in getmembers(package) if ismodule(member) and _modules_utils._is_subpackage_of(member, package)]
	_logger.debug(f"List modules from package {package.__name__}:\n{[module.__name__ for module in list_modules]}")
	if new_package_path is not None and not os.path.exists(new_package_path):
		copy_tree(os.path.dirname(path), new_package_path)

	# create docstrings in the __init__ of package
	create_docstrings_from_module(package, formatter,
									new_path=new_path_module(package, path),
									remove_decorator=remove_decorator,
									decorator_name=decorator_name)

	for module in list_modules:
		if subpackages and os.path.basename(module.__file__) == "__init__.py":
			# document a subpackage
			create_docstrings_from_package(module, formatter, os.path.dirname(new_path_module(module, path)), subpackages, remove_decorator, decorator_name)
		elif os.path.basename(module.__file__) != "__init__.py":
			# create docstrings in the modules found
			create_docstrings_from_module(module, formatter,
									new_path=new_path_module(module, path),
									remove_decorator=remove_decorator,
									decorator_name=decorator_name)

	_logger.info(f"package {package.__name__} was documented with success!")

