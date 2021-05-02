"""Class to define formaters for docstring"""
from inspect import _empty
try:
	import yaml
	yaml_imported = True
except ModuleNotFoundError:
	import json
	yaml_imported = False


class Formatter:
	"""Class to format docstring"""

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
		items_string = []
		for name, value in items_.items():
			name = name if value[1] == _empty else f'OPTIONNAL[{name}]'
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
		kwargs_format = [{
							'prefix': self.prefix_field*len(name),
							'name': name,
							'suffix': self.suffix_field*len(name),
							'items': self._format_items(**values)}
						for name, values in fields.items()]
		fields_string = [self.field_fmt.format(**{k: v for k, v in kw.items() if k in self.field_fmt})
						for kw in kwargs_format]

		return f"\n".join(fields_string).strip()

	def format_docstring(self, nb_base_tab: int = 0, description: str = "{DESCRIPTION}", fields: dict = {}) -> str:
		base_tab = '\t'*nb_base_tab
		docstring = f"{base_tab}\"\"\"{self.description_fmt.format(description=description)}\n{self._format_fields(fields)}\n\"\"\"\n"
		return f"\n{base_tab}".join(docstring.split('\n')).rstrip('\t')

	@staticmethod
	def simple_format() -> Formatter:
		return Formatter()

	@staticmethod
	def numpy_format() -> Formatter:
		return Formatter(suffix_field="-")

	@staticmethod
	def from_config(config_path: str) -> Formatter:
		with open(config_path, 'r') as f:
			if yaml_imported:
				configs = yaml.safe_load(f)
			else:
				configs = json.load(f)

		try:
			formatter =  Formatter(
										description_fmt=configs['description'],
										field_fmt=configs['fields'],
										items_fmt=configs['items'],
										prefix_field=configs['prefix'],
										suffix_field=configs['suffix']
									)
		except KeyError as e:
			raise e
		return formatter

