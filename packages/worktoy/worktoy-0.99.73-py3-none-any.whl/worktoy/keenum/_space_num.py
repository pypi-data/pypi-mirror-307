"""SpaceNum provides the namespace class used by the MetaNum metaclass."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

try:
  from typing import Any, Self, TYPE_CHECKING
except ImportError:
  TYPE_CHECKING = False
  Self = object
  Any = object

from worktoy.keenum import Num
from worktoy.meta import AbstractNamespace, OverloadSpace, CallMeMaybe
from worktoy.parse import maybe
from worktoy.text import monoSpace

if TYPE_CHECKING:
  NumList = list[Num]


class SpaceNum(OverloadSpace):
  """SpaceNum provides the namespace class used by the MetaNum metaclass."""

  __num_entries__ = None
  __reserved_names__ = ['__num_entries__', '__init__', ]

  def _getNumEntries(self) -> NumList:
    """Get the Num entries."""
    return maybe(self.__num_entries__, [])

  def _addNumEntry(self, key: str, num: Num) -> None:
    """Add a Num entry."""
    existing = self._getNumEntries()
    Num.setPrivateValue(num, len(existing))
    Num.setPublicName(num, key)
    self.__num_entries__ = [*existing, num]

  def _validateName(self, name: str) -> str:
    """Validate the name."""
    if name in self.__reserved_names__:
      e = """Received a reserved name: '%s'!""" % name
      raise AttributeError(monoSpace(e))
    if name.lower() in self._getNumEntries():
      e = """Received a name that is already in use: '%s'!""" % name
      raise AttributeError(monoSpace(e))
    return name

  def __setitem__(self, key: str, value: object) -> None:
    """Set the key, value pair."""
    if not getattr(value, '__trust_me_bro__', False):
      key = self._validateName(key)
    if isinstance(value, Num):
      return self._addNumEntry(key, value)
    return OverloadSpace.__setitem__(self, key, value)

  def compile(self, ) -> dict:
    """Compile the namespace."""
    return {**OverloadSpace.compile(self),
            '__num_entries__': self._getNumEntries(),
            '__keenum_list__': [],
            '__keenum_dict__': {}}
