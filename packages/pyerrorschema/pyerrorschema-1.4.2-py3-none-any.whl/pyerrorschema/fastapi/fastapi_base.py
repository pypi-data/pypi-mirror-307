import json
from typing import Any, Dict, List, Optional

from pydantic import Field
from typing_extensions import Self

from ..err_base import ErrorSchema
from ..types import MsgType
from ..utils import restrict_arguments


class FastAPIErrorSchema(ErrorSchema):
    loc: List[str] = Field(default_factory=list)
    input: Dict[str, Any] = Field(default_factory=dict)
    ui_msg: Optional[str] = Field(default=None)

    def to_dict(self, target: MsgType = "backend") -> Dict[str, Any]:
        """Convert the error schema to a dictionary.

        If target is "frontend", only the fields `msg` and `input` are included, and
        if `ui_msg` is not None, the field `msg` is overwritten by `ui_msg`. If target
        is "backend", all fields are included, except for `ui_msg`.

        Args:
            target (MsgType): The target of the error message. The default is "backend".

        Returns:
            error_dict (dict[str, Any]): The error schema as a dictionary.
        """
        error_dict = self.model_dump()

        if target == "frontend":
            error_dict.pop("loc")
            error_dict.pop("type")
            if error_dict["ui_msg"] is not None:
                error_dict["msg"] = error_dict["ui_msg"]

        error_dict.pop("ui_msg")
        return error_dict

    def to_string(self, target: MsgType = "backend") -> str:
        """Convert the error schema to a string.

        Args:
            target (MsgType): The target of the error message. The default is "backend".

        Returns:
            err_str (str): The error schema as a string.
        """
        return json.dumps(self.to_dict(target))

    ### Factory methods ###

    def frontend_variant(self, msg: Optional[str] = None) -> Self:
        """Convert the error schema to a frontend error schema.

        .. caution:: This method will be deprecated in the future.
        """
        modified_schema = self.schema_copy()
        if msg is not None:
            modified_schema.msg = msg
        return modified_schema

    @classmethod
    @restrict_arguments("type")
    def validation_error(cls, **kwargs) -> Self:
        """Factory method to create an instance for a validation error."""
        return cls._create_error("validation_error", "Validation error occurred.", **kwargs)

    @classmethod
    @restrict_arguments("type")
    def value_error(cls, **kwargs) -> Self:
        """Factory method to create an instance for a value error."""
        return cls._create_error("value_error", "Value error occurred.", **kwargs)

    @classmethod
    @restrict_arguments("type")
    def docker_error(cls, **kwargs) -> Self:
        """Factory method to create an instance for a docker error."""
        return cls._create_error("docker_error", "Docker error occurred.", **kwargs)

    @classmethod
    def customized_error(cls, **kwargs) -> Self:
        """Factory method to create an instance for a customized error."""
        return cls._create_error("customized_error", "Customized error occurred.", **kwargs)
