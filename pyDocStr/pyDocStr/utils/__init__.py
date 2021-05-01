from .formatter import Formatter
from . import load_module

try:
	from . import coloredLoggerFormatter
	_colorama_imported = True
except (ImportError, ModuleNotFoundError):
	_colorama_imported = False