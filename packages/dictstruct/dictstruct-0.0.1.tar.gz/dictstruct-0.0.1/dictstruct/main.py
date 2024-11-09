import logging
from contextlib import suppress
from typing import Any, Iterator, Tuple

from msgspec import UNSET, Struct

logger = logging.getLogger(__name__)


class DictStruct(Struct, dict=True):  # type: ignore [call-arg]
    """
    A base class that extends the :class:`msgspec.Struct` class to provide dictionary-like access to struct fields.

    Allows iteration over the fields of a struct and provides a dictionary-like interface for retrieving values by field name.

    Example:
        >>> class MyStruct(DictStruct):
        ...     field1: str
        ...     field2: int
        >>> s = MyStruct(field1="value", field2=42)
        >>> list(s.keys())
        ['field1', 'field2']
        >>> s['field1']
        'value'
    """

    def __bool__(self) -> bool:
        """A Struct will always exist."""
        return True

    def __contains__(self, key: str) -> bool:
        """
        Check if a key is in the struct.

        Args:
            key: The key to check.

        Returns:
            True if the key is present and not :obj:`~UNSET`, False otherwise.
        """
        return key in self.__struct_fields__ and getattr(self, key, UNSET) is not UNSET

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get the value associated with a key, or a default value if the key is not present.

        Args:
            key: The key to look up.
            default (optional): The value to return if the key is not present.

        Returns:
            Any: The value associated with the key, or the default value.
        """
        return getattr(self, key, default)

    def __getitem__(self, attr: str) -> Any:
        """
        Lookup an attribute value via dictionary-style access.

        Args:
            attr: The name of the attribute to access.

        Raises:
            KeyError: If the provided key is not a member of the struct.

        Returns:
            The value of the attribute.
        """
        try:
            return getattr(self, attr)
        except AttributeError:
            raise KeyError(attr, self) from None

    def __getattribute__(self, attr: str) -> Any:
        """
        Get the value of an attribute, raising AttributeError if the value is :obj:`UNSET`.

        Args:
            attr: The name of the attribute to fetch.

        Raises:
            AttributeError: If the value is :obj:`~UNSET`.

        Returns:
            The value of the attribute.
        """
        value = super().__getattribute__(attr)
        if value is UNSET:
            raise AttributeError(
                f"'{type(self).__name__}' object has no attribute '{attr}'"
            )
        return value

    def __iter__(self) -> Iterator[str]:
        """
        Iterate through the keys of the Struct.

        Yields:
            Struct key.
        """
        for field in self.__struct_fields__:
            value = getattr(self, field, UNSET)
            if value is not UNSET:
                yield field

    def __len__(self) -> int:
        """
        The number of keys in the Struct.

        Returns:
            The number of keys.
        """
        return len([key for key in self])

    def keys(self) -> Iterator[str]:
        """
        Returns an iterator over the field names of the struct.

        Returns:
            An iterator over the field names.
        """
        yield from self

    def items(self) -> Iterator[Tuple[str, Any]]:
        """
        Returns an iterator over the struct's field name and value pairs.

        Returns:
            Iterator[Tuple[str, Any]]: An iterator over the field name and value pairs.
        """
        for key in self.__struct_fields__:
            value = getattr(self, key, UNSET)
            if value is not UNSET:
                yield key, value

    def values(self) -> Iterator[Any]:
        """
        Returns an iterator over the struct's field values.

        Returns:
            An iterator over the field values.
        """
        for key in self.__struct_fields__:
            value = getattr(self, key, UNSET)
            if value is not UNSET:
                yield value

    def __hash__(self) -> int:
        """
        A frozen Struct is hashable but only if the fields are all hashable as well.

        This modified hash function converts any list fields to tuples and sets the new hash value.

        Raises:
            TypeError: If the struct is not frozen.

        Returns:
            The hash value of the struct.
        """
        if not self.__struct_config__.frozen:
            raise TypeError(f"unhashable type: '{type(self).__name__}'")
        if cached_hash := self.__dict__.get("__hash__"):
            return cached_hash
        fields = (
            getattr(self, field_name, None) for field_name in self.__struct_fields__
        )
        try:
            # Skip if-checks, just try it
            try:
                self.__dict__["__hash__"] = hash(fields)
            except TypeError:  # unhashable type: 'list'
                self.__dict__["__hash__"] = hash(
                    tuple(f) if isinstance(f, list) else f for f in fields
                )
        except Exception as e:
            e.args = *e.args, "recursed in hash fn"
        return self.__dict__["__hash__"]


class LazyDictStruct(DictStruct, frozen=True):  # type: ignore [call-arg,misc]
    """
    A subclass of DictStruct that supports JIT decoding of field values.

    It exists to optimize performance and memory usage by storing field values in a raw, undecoded format and decoding them only when accessed.

    This class is frozen, meaning its fields cannot be modified after creation.

    Example:
        >>> import msgspec
        >>> from functools import cached_property
        >>> class MyStruct(LazyDictStruct):
        ...     _myField: msgspec.Raw = msgspec.field(name='myField')
        ...     @cached_property
        ...     def myField(self) -> str:
        ...         '''Decode the raw JSON data into a python object when accessed.'''
        ...         return msgspec.json.decode(self._myField, type=str)
        ...
        >>> raw_data = msgspec.json.encode({"myField": "some value"})
        >>> my_struct = MyStruct(_myField=raw_data)
        >>> print(my_struct.myField)
        "some value"
    """

    def __init_subclass__(cls, *args, **kwargs):
        """
        Initialize a subclass of LazyDictStruct.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.
        """
        super().__init_subclass__(*args, **kwargs)

        if cls.__name__ == "StructMeta":
            return

        try:
            struct_fields = cls.__struct_fields__
        except AttributeError:
            # TODO: debug this
            # raise TypeError(cls, dir(cls), issubclass(cls, Struct))
            return

        resolved_fields = tuple(
            field[1:] if field[0] == "_" else field for field in struct_fields
        )
        cls.__struct_fields__ = resolved_fields
