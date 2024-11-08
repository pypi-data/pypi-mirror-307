import textwrap
from copy import deepcopy
from typing import Any, List, Union

from typing_extensions import Self

from .err_base import ErrorSchema


class ErrGroup:
    def __init__(self) -> None:
        self._error_schemas: list = []

    @property
    def error_schemas(self) -> list:
        return self._error_schemas

    def copy(self) -> Self:
        """Create a copy of the error group."""
        return deepcopy(self)

    def clear(self) -> None:
        """Clear all error schemas from the group."""
        self._error_schemas.clear()

    def __repr__(self) -> str:
        errors_repr = ',\n'.join(repr(error) for error in self._error_schemas)
        indented_errors = textwrap.indent(errors_repr, '    ')
        return f"{self.__class__.__name__}(\n{indented_errors}\n)"

    def __len__(self) -> int:
        return len(self._error_schemas)

    def __iter__(self):
        return iter(self._error_schemas)

    def __getitem__(self, index):
        return self._error_schemas[index]

    def __setitem__(self, index: int, value) -> None:
        if not isinstance(value, ErrorSchema):
            raise ValueError("The error schema must be an instance of ErrorSchema.")
        self._error_schemas[index] = value

    ## Methods for converting the error schemas ##

    def to_dict(self) -> List[dict]:
        """Convert the error schemas to a dictionary.

        .. note:: This method is deprecated. Use `to_dicts` instead.
        """
        return [err.to_dict() for err in self._error_schemas]

    def to_dicts(self) -> List[dict]:
        """Convert the error schemas to a dictionary."""
        return [err.to_dict() for err in self._error_schemas]

    def to_string(self) -> str:
        """Convert the error schemas to a string."""
        return f"[{', '.join(err.to_string() for err in self._error_schemas)}]"

    def to_list(self) -> list:
        """Convert the error schemas to a list."""
        return deepcopy(self._error_schemas)

    ## Methods for modifying the error schemas ##

    def append(self, error_schema: Any) -> None:
        """Add an error schema to the group."""
        if not isinstance(error_schema, ErrorSchema):
            raise ValueError("The error schema must be an instance of ErrorSchema.")
        self._error_schemas.append(error_schema)

    def extend(self, error_schemas: Union[list, Self]) -> None:
        """Add a list of error schemas to the group."""
        if isinstance(error_schemas, ErrGroup):
            self._error_schemas.extend(error_schemas.to_list())
        elif isinstance(error_schemas, list):
            if not all(isinstance(err, ErrorSchema) for err in error_schemas):
                raise ValueError("All elements must be instances of ErrorSchema.")
            self._error_schemas.extend(error_schemas)
        else:
            raise ValueError("The argument must be a list or an instance of ErrGroup.")

    ## Other utility methods ##

    def concat_messages(self, separator: str = ';') -> str:
        """Concatenate the messages of the error schemas in the group."""
        return f'{separator} '.join(err.msg for err in self._error_schemas)

    def contains_type(self, error_type: str) -> bool:
        """Check if the error group contains an error schema with a specific type."""
        return any(err.type == error_type.lower() for err in self._error_schemas)

    def has_errors(self) -> bool:
        """Check if the error group contains any error schemas."""
        return bool(self._error_schemas)
