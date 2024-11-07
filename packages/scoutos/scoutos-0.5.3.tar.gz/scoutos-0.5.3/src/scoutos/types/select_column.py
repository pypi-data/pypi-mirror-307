# This file was auto-generated by Fern from our API Definition.

from ..core.unchecked_base_model import UncheckedBaseModel
import typing
from .select_option_item import SelectOptionItem
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class SelectColumn(UncheckedBaseModel):
    column_id: typing.Optional[str] = None
    column_display_name: typing.Optional[str] = None
    column_type: typing.Literal["select"] = "select"
    data_type: typing.Optional[typing.Literal["string"]] = None
    hidden: typing.Optional[bool] = None
    options: typing.List[SelectOptionItem]
    selected_option: typing.Optional[int] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
