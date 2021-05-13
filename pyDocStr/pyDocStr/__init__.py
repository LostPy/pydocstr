import os
import logging as _logging

from . import utils
from .documented import FunctionToDocument, ClassToDocument
from .documented import to_document


if utils._colorama_imported:
	_log_fmt = utils.coloredLoggerFormatter.ColoredFormatter(fmt="[%(asctime)s][%(name)s][%(levelname)s] %(message)s", datefmt="%H:%M:%S")
else:
	_log_fmt = _logging.Formatter(fmt="[%(asctime)s][%(name)s][%(levelname)s] %(message)s", datefmt="%H:%M:%S")
_logger = _logging.getLogger('pyDocStr')
_handler = _logging.StreamHandler()
_handler.setFormatter(_log_fmt)
_logger.addHandler(_handler)
_logger.setLevel(_logging.DEBUG)


from .build_docstrings import create_docstrings_from_module, create_docstrings_from_folder, create_docstrings_from_package


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


#@to_document(description="A function to get a formatter with the name")
def get_formatter(name: str):
	formatters = {
		'simple': utils.Formatter.simple_format(),
		'numpy': utils.Formatter.numpy_format()
	}
	return formatters[name.lower()]


def _formatter_from_config_path(config_path: str):
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


#@to_document(description="A function to build docstrings for a package.\nThis function should be called in a main fille which import the package.")
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