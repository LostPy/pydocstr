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


from .build_docstrings import create_docstrings_from_file, create_docstrings_from_folder


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

