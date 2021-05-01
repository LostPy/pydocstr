"""Class to define formaters for docstring"""
from inspect import _empty


class Formatter:
	"""Class to format docstring"""

	def __init__(self, description_fmt: str = "{description}\n",
				field_fmt: str = "{prefix}\n{name}\n{suffix}\n{values}",
				items_fmt: str = "\t{name} : {type}\n\t\t{description}\n\t\t{default}",
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
			items_string.append(self.items_fmt.format(name=name, type=type_, default=default, description="{DESCRIPTION}").rstrip())

		return f"\n".join(items_string) if len(items_string) > 0 else None

	def _format_fields(self, fields: dict = {}) -> str:
		fields_string = [self.field_fmt.format(prefix=self.prefix_field*len(name), name=name,
						suffix=self.suffix_field*len(name), values=self._format_items(**values))
						for name, values in fields.items()]

		return f"\n".join(fields_string).strip()

	def format_docstring(self, nb_base_tab: int = 0, description: str = "{DESCRIPTION}", fields: dict = {}) -> str:
		base_tab = '\t'*nb_base_tab
		docstring = f"{base_tab}\"\"\"{self.description_fmt.format(description=description)}\n{self._format_fields(fields)}\n\"\"\"\n"
		return f"\n{base_tab}".join(docstring.split('\n')).rstrip('\t')

	@staticmethod
	def simple_format():
		return Formatter()

	@staticmethod
	def numpy_format():
		return Formatter(suffix_field="-")