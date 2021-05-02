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
		# Import of module from path
		path = path.replace('\\', '/')
		module_name = path.split('/')[-1].split('.')[0]
		spec = spec_from_file_location(module_name, path)
		module = module_from_spec(spec)
		spec.loader.exec_module(module)
		return module
	except ImportError as e:
		raise e

