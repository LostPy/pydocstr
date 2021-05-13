from .formatter import Formatter
from . import _modules_utils

try:
	from . import coloredLoggerFormatter
	_colorama_imported = True
except (ImportError, ModuleNotFoundError):
	_colorama_imported = False