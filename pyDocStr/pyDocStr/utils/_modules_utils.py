import os
from importlib import import_module
from importlib.util import spec_from_file_location, module_from_spec
from inspect import getmembers


def _import_from_path(path: str):
	"""A function to load a module from a path.
	
	Parameters
	----------
	path : str
		The path of module to load.
	
	Returns
	-------
	module : Module
		The module imported.
	"""
	try:
		path = path.replace('\\', '/').rstrip('/')
		path = os.path.abspath(path)
		module_name = path.split('/')[-1].split('.')[0]
		if os.path.isdir(path):  # if the path is the path of a package
			path = os.path.join(path, '__init__.py')
		spec = spec_from_file_location(module_name, path)
		module = module_from_spec(spec)
		print(module)
		spec.loader.exec_module(module)

		return module
	except ImportError as e:
		raise e


def _is_subpackage_of(package, parent):
	"""A function check if a package is a package imported from environment or a subpackage of a parent package.
	
	Parameters
	----------
	package : module
		The package to check if it's a subpackage of 'parent'
	parent : module
		A package which had imported 'package' 
	
	Returns
	-------
	result : bool
		The result of test.
	"""

	package_path = os.path.abspath(package.__file__)
	parent_path = os.path.abspath(parent.__file__)
	return os.path.commonpath([package_path, parent_path]) == os.path.dirname(parent_path)
