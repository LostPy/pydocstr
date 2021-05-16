import os
import logging as _logging

from . import utils
from .documented import FunctionToDocument, ClassToDocument
#from .documented import to_document


if utils._colorama_imported:
	_log_fmt = utils.coloredLoggerFormatter.ColoredFormatter(fmt="[%(asctime)s][%(name)s][%(levelname)s] %(message)s", datefmt="%H:%M:%S")
else:
	_log_fmt = _logging.Formatter(fmt="[%(asctime)s][%(name)s][%(levelname)s] %(message)s", datefmt="%H:%M:%S")
_logger = _logging.getLogger('pyDocStr')
_handler = _logging.StreamHandler()
_handler.setFormatter(_log_fmt)
_logger.addHandler(_handler)
_logger.setLevel(_logging.DEBUG)


from .build_docstrings import create_docstrings_from_module, create_docstrings_from_package


def set_level_logger(levelname: str):
	"""A function to set the level logger

	Parameters
	----------
	levelname : str
		The level of logger
	"""
	levels = {
		'debug': _logging.DEBUG,
		'info': _logging.INFO,
		'warning': _logging.WARNING,
		'error': _logging.ERROR,
		'critical': _logging.CRITICAL
	}

	_logger.setLevel(levels[levelname])


def get_formatter(name: str):
	"""A function to get an existing formatter with the name.

	Parameters
	----------
	name : str
		The name of formatter. Choices: 'simple', 'numpy'

	Returns
	-------
	formatter : Formatter
		The formatter instance.
	"""
	formatters = {
		'simple': utils.Formatter.simple_format(),
		'numpy': utils.Formatter.numpy_format()
	}
	return formatters[name.lower()]


def _formatter_from_config_path(config_path: str):
	"""Create a custom formatter with a config file.

	Parameters
	----------
	config_path : str
		The path of config file. This file must be a json file or a yaml file.

	Returns
	-------
	formatter : Formatter
		The formatter created.
	"""
	if os.path.exists(config_path):
		try:
			return utils.Formatter.from_config(config_path)
		except KeyError:
			_logger.error("KeyError was raised in configuration file."\
					" The file must contain the following keywords: 'description', 'fields', 'items', 'prefix', 'suffix'.")
			_logger.debug(traceback.format_exc())
			return None
		except json.JSONDecodeError:
			_logger.error("A JSONDecodeError was raised. Check the config file. json module can only read json files.")
			_logger.debug(traceback.format_exc())
			return None
		except YAMLError:
			_logger.error("A YAMLError was raised. Check the config file. yaml module can read json and yaml (yml) files.")
			_logger.debug(traceback.format_exc())
			return None
		except Exception as e:
			_logger.error("An exception was raised while reading the configuration file. Check the config file.")
			_logger.error(traceback.format_exc())
			return None
	_logger.error(f'The config file was not found: {config_path}')
	return None


def build_docstrings_package(
								package,
								formatter = utils.Formatter.simple_format(),
								config_formatter: str = None,
								new_package_path: str = None,
								subpackages: bool = False,
								remove_decorator: bool = True,
								decorator_name: str = 'to_document',
								level_logger: str = 'info',
							):
	"""Build all docstring for a package.

	Parameters
	----------
	package : module
		The package to document
	OPTIONAL[formatter] : Union[str, Formatter]
		The formatter name or the formatter to use. Use if config_formatter is not used.
		Default: None
	OPTIONAL[config_formatter] : str
		The path of config file for the formatter. This file must be a json file or a yaml file.
		Default: None
	OPTIONAL[new_package_path] : str
		The folder path where the package documented must be saved. If None, the package is overwritten.
		Default: None
	OPTIONAL[subpackages] : bool
		If True, all subpackages are documented.
		Default: False
	OPTIONAL[remove_decorator] : bool
		If True, the decorators 'to_document' are removed.
		Default: True
	OPTIONAL[decorator_name] : str
		The name use for decorator 'to_document'.
		Default: 'to_document'
	OPTIONAL[level_logger] : str
		The level of logger. Choices: 'debug', 'info', 'warning', 'error'
		Default: 'info'

	Returns
	-------
	None
	"""

	if config_formatter is None and isinstance(formatter, str):
		formatter = get_formatter(formatter)
	elif config_formatter is not None:
		formatter = _formatter_from_config_path(config_formatter)
		if formatter is None:
			return
	elif not isinstance(formatter, utils.Formatter):
		raise ValueError(f"'formatter' must be an instance of 'str' or of 'Formatter', not '{type(formatter)}'")

	set_level_logger(level_logger)
	return create_docstrings_from_package(package, formatter, new_package_path, subpackages=subpackages,
										remove_decorator=remove_decorator, decorator_name=decorator_name)