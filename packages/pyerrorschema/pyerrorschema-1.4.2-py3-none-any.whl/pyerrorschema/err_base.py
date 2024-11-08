import inspect
import json
import textwrap
from typing import Any, Dict, List

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Self, TypeVar

from .utils import restrict_arguments

ErrorSchemaType = TypeVar("ErrorSchemaType", bound="ErrorSchema")


class ErrorSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: str = Field(default="")
    msg: str = Field(default="")

    def __repr__(self) -> str:
        attrs = [f"{k}={repr(v)}" for k, v in self.__dict__.items() if not k.startswith('_')]
        attrs_str = textwrap.indent(',\n'.join(attrs), '    ')
        return f"{self.__class__.__name__}(\n{attrs_str}\n)"

    def __str__(self) -> str:
        return self.__repr__()

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()

    def to_string(self) -> str:
        """Convert the error schema to a string."""
        return json.dumps(self.to_dict())

    def schema_copy(self) -> Self:
        """Create a deep copy of the error schema."""
        return self.__class__(**self.model_dump())

    @classmethod
    def list_available_errors(cls) -> List[str]:
        """List all available error types."""
        return [
            name for name, _ in inspect.getmembers(cls, predicate=inspect.ismethod)
            if name.endswith("_error") and not name.startswith("_")
        ]

    @staticmethod
    def wrapping_string(error_schemas: List[ErrorSchemaType]) -> str:
        """Wraps the error schemas in a string representation.

        This method is used to wrap a list of error schemas in a string representation. The resulting string
        is a JSON array of error schemas. The error schemas must be instances of ErrorSchema.

        Args:
            error_schemas (List[ErrorSchema]): List of error schemas.

        .. caution:: This method will be deprecated in the future.
        """
        if isinstance(error_schemas, ErrorSchema):
            error_schemas = [error_schemas]
        if isinstance(error_schemas, list):
            if all(isinstance(err, ErrorSchema) for err in error_schemas):
                return f"[{', '.join(err.to_string() for err in error_schemas)}]"
            else:
                raise ValueError("All elements in the list must be instances of ErrorSchema.")
        else:
            raise ValueError("The argument must be an instance of ErrorSchema or a list of ErrorSchema instances.")

    ### Factory methods ###

    @classmethod
    def _create_error(cls, error_type: str, default_msg: str, **kwargs) -> Self:
        """Base factory method to create an instance for an error."""
        defaults = {
            "type": error_type,
            "msg": default_msg,
        }
        defaults.update(kwargs)
        return cls(**defaults)

    @classmethod
    @restrict_arguments("type")
    def database_error(cls, **kwargs) -> Self:
        """Factory method to create an instance for a database error."""
        return cls._create_error("database_error", "Database error occurred.", **kwargs)

    @classmethod
    @restrict_arguments("type")
    def file_error(cls, **kwargs) -> Self:
        """Factory method to create an instance for a file error."""
        return cls._create_error("file_error", "File error occurred.", **kwargs)

    @classmethod
    @restrict_arguments("type")
    def runtime_error(cls, **kwargs) -> Self:
        """Factory method to create an instance for a runtime error."""
        return cls._create_error("runtime_error", "Runtime error occurred.", **kwargs)

    @classmethod
    @restrict_arguments("type")
    def parse_error(cls, **kwargs) -> Self:
        """Factory method to create an instance for a parse error."""
        return cls._create_error("parse_error", "Parse error occurred.", **kwargs)
