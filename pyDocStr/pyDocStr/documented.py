"""Class to define a fonction or class which must be documented.
A Decorator is used to indicate if the functions or class must be documented or not"""
from inspect import getsource, getmembers, isfunction, ismethod, isclass, signature, _empty, isbuiltin


#@to_document(description="A base class for objects to document.")
class ObjectToDocument:
	def __init__(self, func_or_class, description: str = ""):
		self.obj = func_or_class
		self.name = self.obj.__name__
		self.description = description

	def __str__(self):
		return f"<type='{type(self).__name__}' | name='{self.name}'>"

	def __repr__(self):
		return self.__str__()

	def __call__(self, *args, **kwargs):
		return self.obj(*args, **kwargs)


#@to_document(description="A class to represent a function to document.")
class FunctionToDocument(ObjectToDocument):
	def __init__(self, func_, description: str = "",
				name_return: str = "result", **kwargs):
		ObjectToDocument.__init__(self, func_, description)
		sign = signature(self.obj)
		self.parameters = {name: (param.annotation, param.default) for name, param in sign.parameters.items() if name != 'self'}
		self.returns = {name_return: (sign.return_annotation, _empty)} if sign.return_annotation != _empty else {}
		self.description_parameters = kwargs
		del(sign)

		source = getsource(func_)
		self.nb_base_tab = source[:source.find('def')].count('\t') // 2 + 1  # 1 indentations in python file count for 2 ? (test)
		del(source)


#@to_document(description="A class to represent a class with this methods to documents.")
class ClassToDocument(ObjectToDocument):
	def __init__(self, class_, description: str = "", **kwargs):
		ObjectToDocument.__init__(self, class_, description)
		self.methods_to_document = []
		self.attributes = {name: (_empty, _empty) for name in dir(class_) if not name.startswith('_')}

		self.public_methods, self.protected_methods = {}, {}
		members = [member for member in getmembers(class_, predicate=self._isfunction_or_isfunctiontodocument) if not member[0].startswith(('__'))]
		for name, method in members:
			# Create the list of methods, attributes and methods to document
			if isinstance(method, FunctionToDocument):
				type_default = (signature(method.obj).return_annotation, _empty)
				self.methods_to_document.append(method)
			else:
				type_default = (signature(method).return_annotation, _empty)

			if not name.startswith('_'):
				self.public_methods[name] = type_default
			else:
				self.protected_methods[name] = type_default

		if len(members) > 0:
			# If there is 1 method or more, we use this method to count the number of indentation
			source = getsource(members[0][1].obj if isinstance(members[0][1], FunctionToDocument) else members[0][1])
		else:
			# Else, we use the __init__ methods
			try:
				source = getsource(class_.__init__)
			except TypeError:  # If __init__ is not defined
				source = None
		self.nb_base_tab = source[:source.find('def')].count('\t') - 1if source is not None else 1
		del(source)
		del(members)

#	@to_document(description="Return if an object is a function or a FunctionToDocument.")
	@staticmethod
	def _isfunction_or_isfunctiontodocument(obj) -> bool:
		return isfunction(obj) or isinstance(obj, FunctionToDocument)


def to_document(description: str = "", **kwargs):
	# A decorator to transform a function or a class in a FunctionToDocument or ClassToDocument.
	# If object is not a function and is not a class: return the object
	def decorator(obj):
		if isfunction(obj) or ismethod(obj):
			return FunctionToDocument(obj, description, **kwargs)
		elif isclass(obj):
			return ClassToDocument(obj, description, **kwargs)
		else:
			return obj
	return decorator

