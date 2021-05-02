"""Class to define formaters for docstring"""
from inspect import _empty
try:
	import yaml
	yaml_imported = True
except ModuleNotFoundError:
	yaml_imported = False
finally:
	import json


class Formatter:
	"""Class to format docstrings.
	
	Attributes
	----------
	description_fmt : str
		The format of description in a docstring.
	field_fmt : str
		The format of a field of docstring.
	items_fmt : str
		The format of an item of fields.
	prefix_field : str
		The prefix to add before names field.
	suffix_field : str
		The suffix to add after names field.
	
	Public methods
	--------------
	format_docstring : str
		A method to format a docstring.
	from_config : Formatter
		A static method to get a Formatter with a config file.
	numpy_format : Formatter
		A static method to get a numpy Formatter
	simple_format : Formatter
		A static method to get the default Formatter
	
	Protected methods
	-----------------
	_format_fields : str
		A method to format fields of a docstring.
	_format_items : str
		A method to format items of a field.
	"""

	def __init__(self, description_fmt: str = "{description}\n",
				field_fmt: str = "{prefix}\n{name}\n{suffix}\n{items}",
				items_fmt: str = "{name} : {type}\n\t{description}\n\t{default}",
				prefix_field: str = "",
				suffix_field: str = ""):
		self.description_fmt = description_fmt
		self.field_fmt = field_fmt
		self.items_fmt = items_fmt
		self.prefix_field = prefix_field
		self.suffix_field = suffix_field

	def _format_items(self, **items_) -> str:
		"""Return a str with items {name: (type, value)} with the format specify by 'self.items_fmt'.
		
		Parameters
		----------
		items_ : Keywords arguments
			Items of a field to format.
			It's a dictionary with the name of item in key and a tuple (type, default) in value
		
		Returns
		-------
		result : str
			Items formatted.
		"""
		items_string = []
		for name, value in items_.items():
			name = name if value[1] == _empty else f'OPTIONAL[{name}]'
			if value[0] == _empty:
				type_ = '{TYPE}'
			elif isinstance(value[0], type):
				type_ = value[0].__name__
			else:
				type_ = str(value[0]).replace('typing.', '')
			default=f'Default: {value[1]}' if value[1] != _empty else ''
			kwargs_format = {'name': name, 'type': type_, 'default': default, 'description': "{DESCRIPTION}"}
			items_string.append(self.items_fmt.format(**{k: v for k, v in kwargs_format.items() if k in self.items_fmt}).rstrip())

		return f"\n".join(items_string) if len(items_string) > 0 else None

	def _format_fields(self, fields: dict = {}) -> str:
		"""Return a str with fields {name: items} with the format specify by 'self.field_fmt'.
		
		Parameters
		----------
		OPTIONAL[fields] : dict
			Fields of docstring to format.
			It's a dictionary with name of fields in key and in value a dictionary of items.
			Default: {}
		
		Returns
		-------
		result : str
			Fields formatted
		"""
		kwargs_format = [{
							'prefix': self.prefix_field*len(name),
							'name': name,
							'suffix': self.suffix_field*len(name),
							'items': self._format_items(**items)}
						for name, items in fields.items()]
		fields_string = [self.field_fmt.format(**{k: v for k, v in kw.items() if k in self.field_fmt})
						for kw in kwargs_format]

		return f"\n".join(fields_string).strip()

	def format_docstring(self, nb_base_tab: int = 0, description: str = "{DESCRIPTION}", fields: dict = {}) -> str:
		"""Return the docstring with the description and fields specified.
		
		Parameters
		----------
		OPTIONAL[nb_base_tab] : int
			The number of indentation of the signature function/class
			Default: 0
		OPTIONAL[description] : str
			The description of the docstring
			Default: "{DESCRIPTION}"
		OPTIONAL[fields] : dict
			Fields to format. It's a dictionary with name of fields in key and in value a dictionary of items
			Default: {}
		
		Returns
		-------
		result : str
			The docstring created.
		"""
		base_tab = '\t'*nb_base_tab
		docstring = f"{base_tab}\"\"\"{self.description_fmt.format(description=description)}\n{self._format_fields(fields)}\n\"\"\"\n"
		return f"\n{base_tab}".join(docstring.split('\n')).rstrip('\t')

	@staticmethod
	def simple_format():
		"""A staticmethod to get the default Formatter.
		
		Parameters
		----------
		None
		
		Returns
		-------
		Formatter
		"""
		return Formatter()

	@staticmethod
	def numpy_format():
		"""A staticmethod to get the numpy Formatter.
		
		Parameters
		----------
		None
		
		Returns
		-------
		Formatter
		"""
		return Formatter(suffix_field="-")

	@staticmethod
	def from_config(config_path: str):
		"""A staticmethod to get a custom Formatter built with a config file.
		
		Parameters
		----------
		config_path : str
			The path of config file. A yaml or json file.
		
		Returns
		-------
		Formatter
		"""
		with open(config_path, 'r') as f:
			if yaml_imported and (config_path[-4:] == '.yml' or config_path[-5:] == '.yaml'):
				configs = yaml.safe_load(f)
			else:
				configs = json.load(f)

		
		try:
			kwargs = {
				'description_fmt': configs['description'],
				'field_fmt': configs['fields'],
				'items_fmt': configs['items'],
				'prefix_field': configs['prefix'],
				'suffix_field': configs['suffix']
			}
		except KeyError as e:
			raise e
		return Formatter(**{k: v for k, v in kwargs.items() if v is not None})

