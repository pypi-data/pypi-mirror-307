"""Field class subclasses the 'AbstractDescriptor' and provides the owning
class with decorators for explicitly specifying the accessor methods. This
means that the owning class are free to customize accessor method for each
of their attributes. The GET, SET, DELETE and RESET decorators allow the
owning class to designate the methods responsible for accessor operations.
Besides these decorators, the Field class also inherits the notification
related decorators from the AbstractDescriptor class. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

try:
  from typing import Callable, Any
except ImportError:
  Callable = object
  Any = object

from worktoy.desc import AbstractDescriptor
from worktoy.text import typeMsg


class Field(AbstractDescriptor):
  """Field provides a flexible implementation of the descriptor
  protocol allowing owning classes to decorate methods as accessor
  methods. """
  __field_type__ = None
  #  Accessor methods
  __getter_function__ = None
  __setter_function__ = None
  __resetter_function__ = None
  __deleter_function__ = None
  #  Keys for accessor methods
  __getter_key__ = None
  __setter_key__ = None
  __resetter_key__ = None
  __deleter_key__ = None

  def __set_name__(self, owner: type, name: str) -> None:
    """Set the name of the field and the owner of the field."""
    self.__field_owner__ = owner
    self.__field_name__ = name
    if self.__getter_key__ is not None:
      self.__getter_function__ = getattr(owner, self.__getter_key__, None)
    if self.__setter_key__ is not None:
      self.__setter_function__ = getattr(owner, self.__setter_key__, None)
    if self.__resetter_key__ is not None:
      self.__resetter_function__ = getattr(
          owner, self.__resetter_key__, None)
    if self.__deleter_key__ is not None:
      self.__deleter_function__ = getattr(owner, self.__deleter_key__, None)

  def getFieldType(self) -> type:
    """Getter-function for the field type."""
    if self.__field_type__ is None:
      return object
    if isinstance(self.__field_type__, type):
      return self.__field_type__
    e = typeMsg('__field_type__', self.__field_type__, type)
    raise TypeError(e)

  def __instance_get__(self, instance: object) -> object:
    """Get the instance object."""
    return self.__get_getter__()(instance)

  def __instance_set__(self, instance: object, value: object) -> None:
    """Set the instance object."""
    self.__get_setter__()(instance, value)

  def __instance_del__(self, instance: object) -> None:
    """Delete the instance object."""
    self.__get_deleter__()(instance)

  def __get_getter__(self, ) -> Callable:
    """Getter-function for the getter-function, getter-ception."""
    if self.__getter_function__ is None:
      e = typeMsg('getter', self.__getter_function__, Callable)
      raise TypeError(e)
    return self.__getter_function__

  def __get_setter__(self, ) -> Callable:
    """Getter-function for the setter-function of the field."""
    if self.__setter_function__ is None:
      e = typeMsg('setter', self.__setter_function__, Callable)
      raise TypeError(e)
    return self.__setter_function__

  def __get_deleter__(self, ) -> Callable:
    """Getter-function for the deleter-function of the field."""
    if self.__deleter_function__ is None:
      e = typeMsg('deleter', self.__deleter_function__, Callable)
      raise TypeError(e)
    return self.__deleter_function__

  def __set_getter__(self, callMeMaybe: Callable) -> Callable:
    """Set the getter function of the field."""
    self.__getter_key__ = callMeMaybe.__name__
    return callMeMaybe

  def __set_setter__(self, callMeMaybe: Callable) -> Callable:
    """Set the setter function of the field."""
    self.__setter_key__ = callMeMaybe.__name__
    return callMeMaybe

  def __set_deleter__(self, callMeMaybe: Callable) -> Callable:
    """Set the deleter function of the field."""
    self.__deleter_key__ = callMeMaybe.__name__
    return callMeMaybe

  def GET(self, callMeMaybe: Callable) -> Callable:
    """Decorator for setting the getter function of the field."""
    return self.__set_getter__(callMeMaybe)

  def SET(self, *args) -> Any:
    """Decorator for setting the setter function of the field."""
    for arg in args:
      if callable(arg):
        return self.__set_setter__(arg)
      if isinstance(arg, str):
        self.__setter_key__ = arg

  def DELETE(self, callMeMaybe: Callable) -> Callable:
    """Decorator for setting the deleter function of the field."""
    return self.__set_deleter__(callMeMaybe)
