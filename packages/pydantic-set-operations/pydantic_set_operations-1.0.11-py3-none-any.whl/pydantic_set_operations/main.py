from typing import Any, Callable, Type

from pydantic import BaseModel, ConfigDict, create_model


class ExtendedBaseModel(BaseModel):
	"""
	A subclass of BaseModel that adds advanced operations for field union, exclusion,
	and difference. This class supports bitwise operators (|, &, -) between instances,
	where the left instance (self) takes precedence for both values and data types.
	"""
	
	@classmethod
	def union(
		cls, _name: str,
		other: 'ExtendedBaseModel',
		__config__: ConfigDict | dict[str] = None,
		__validators__: dict[str, Callable[..., Any]] | None = None
	) -> Type['ExtendedBaseModel']:
		"""
		Creates a new model that merges fields from the current class and another
		ExtendedBaseModel class. In case of overlapping fields, values and data types
		from the current model (self) take precedence.
		
		Args:
			_name (str): The name for the new model.
			other (ExtendedBaseModel): Another model to merge fields with.
			__config__ (ConfigDict): A Pydantic's config dictionary to use.
			__validators__ (dict[str, Callable[..., Any]]): A Pydantic's validators'.
		
		Returns:
			ExtendedBaseModel: A new model including fields from both the current class and
			the other model.
		"""
		# Merge annotations from both models, with precedence for the current class
		fields_data = {*other.__annotations__.items(), *cls.__annotations__.items()}
		# Construct new fields with types and make them required (indicated by `...`)
		new_fields = {field: (annotation, ...) for field, annotation in fields_data}
		return create_model(
			_name,
			__base__=cls,
			__config__=__config__,
			__validators__=__validators__,
			**new_fields
		)
	
	@classmethod
	def omit(
		cls, _name: str,
		__config__: ConfigDict | dict[str] = None,
		__validators__: dict[str, Callable[..., Any]] | None = None,
		*excluded_fields: str
	) -> Type['ExtendedBaseModel']:
		"""
		Exclude specified fields from the current model to create a new model with
		only the remaining fields.
		
		Args:
			_name (str): The name for the new model.
			__config__ (ConfigDict): A Pydantic's config dictionary to use.
			__validators__ (dict[str, Callable[..., Any]]): A Pydantic's validators'.
			*excluded_fields (str): Fields to exclude from the model.
		
		Returns:
			ExtendedBaseModel: A new model excluding the specified fields.
		"""
		# Filter out fields specified in excluded_fields
		new_fields = {
			field: (cls.__annotations__[field], ...)
			for field in cls.__annotations__
			if field not in excluded_fields
		}
		return create_model(
			_name,
			__base__=cls,
			__config__=__config__,
			__validators__=__validators__,
			**new_fields
		)
	
	@classmethod
	def pick(
		cls, _name: str,
		__config__: ConfigDict | dict[str] = None,
		__validators__: dict[str, Callable[..., Any]] | None = None,
		*included_fields: str
	) -> Type['ExtendedBaseModel']:
		"""
		Generate a new model with only the specified fields from the current model.
		
		Args:
			_name (str): The name for the new model.
			__config__ (ConfigDict): A Pydantic's config dictionary to use.
			__validators__ (dict[str, Callable[..., Any]]): A Pydantic's validators'.
			*included_fields (str): Fields to include in the new model.
		
		Returns:
			ExtendedBaseModel: A new model containing only the specified fields.
		"""
		# Select fields specified in included_fields
		new_fields = {
			field: (cls.__annotations__[field], ...)
			for field in cls.__annotations__
			if field in included_fields
		}
		return create_model(
			_name,
			__base__=cls,
			__config__=__config__,
			__validators__=__validators__,
			**new_fields
		)
	
	def __and__(self, other: 'ExtendedBaseModel') -> 'ExtendedBaseModel':
		"""
		Creates a new instance containing only fields common to both the current
		model (self) and another model. For common fields, values and data types
		from the current model take precedence.
		
		Args:
			other (ExtendedBaseModel): Another model to find common fields with.
		
		Returns:
			ExtendedBaseModel: A new model with fields shared by both models, taking values
			and data types from the current model for overlapping fields.
		"""
		# Dump current and other model data into dictionaries
		self_dump = self.model_dump()
		other_dump = other.model_dump()
		# Find common fields between both models
		fields = self_dump.keys() & other_dump.keys()
		# Build data for the new model using values from self
		data = {field: self_dump[field] for field in fields}
		# Use pick to create a new model with the common fields
		return self.pick(
			self.__repr_name__(),
			*fields,
			self.model_config
		)(**data)
	
	def __sub__(self, other: 'ExtendedBaseModel') -> 'ExtendedBaseModel':
		"""
		Creates a new instance by excluding fields present in another model from
		the current model (self).
		
		Args:
			other (ExtendedBaseModel): Another model whose fields will be excluded
			from the current model.
		
		Returns:
			ExtendedBaseModel: A new model without fields that exist in the other model.
		"""
		# Use omit to exclude fields present in the other model
		return self.omit(
			self.__repr_name__(),
			*other.model_dump().keys(),
			self.model_config
		)(**self.model_dump())
	
	def __or__(self, other: 'ExtendedBaseModel') -> BaseModel:
		"""
		Combines fields from the current model (self) and another model. For fields
		present in both models, values and data types from the current model (self)
		take precedence.
		
		Args:
			other (ExtendedBaseModel): Another model to merge fields with.
		
		Returns:
			ExtendedBaseModel: A new model that includes all fields from both models, giving
			priority to values and types from the current model for common fields.
		"""
		# Dump current and other model data into dictionaries
		self_dump = self.model_dump()
		other_dump = other.model_dump()
		# Merge data, prioritizing values from self
		data = {**other_dump, **self_dump}
		# Use union to create a new model with all fields
		return self.union(
			self.__repr_name__(),
			other,
			self.model_config
		)(**data)