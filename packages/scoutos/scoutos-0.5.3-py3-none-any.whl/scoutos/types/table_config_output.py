# This file was auto-generated by Fern from our API Definition.

from ..core.unchecked_base_model import UncheckedBaseModel
import typing
from .table_config_output_schema_item import TableConfigOutputSchemaItem
import pydantic
from ..core.pydantic_utilities import IS_PYDANTIC_V2


class TableConfigOutput(UncheckedBaseModel):
    table_display_name: typing.Optional[str] = None
    table_img_url: typing.Optional[str] = None
    table_description: typing.Optional[str] = None
    schema_: typing.Optional[typing.List[TableConfigOutputSchemaItem]] = pydantic.Field(alias="schema", default=None)

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
