from typing import Callable
from inspect import signature
#
#
#
#
def get_function_parameters(function_: Callable, excluding_parameters: list[str] = None):
	"""

	:param function_: a function to search for parameters in
	:param excluding_parameters: parameters to not include
	:return: function parameters
	:rtype: dict[str, Any]
	"""
	if excluding_parameters is None:
		excluding_parameters = []

	return {key: value for key, value in signature(function_).parameters.items() if key not in excluding_parameters}
#
#
#
#
def get_class_fields(class_, excluding_fields: list[str] = None):
	"""

	:param class_: a class to search for fields in
	:param excluding_fields: fields to not include
	:return: class fields
	:rtype: dict[str, Any]
	"""
	if excluding_fields is None:
		excluding_fields = []

	return {
		key: value for key, value in class_.__dict__.items() if not key.startswith('__') and not key.endswith('__') and not callable(getattr(class_, key)) and key not in excluding_fields
	}
