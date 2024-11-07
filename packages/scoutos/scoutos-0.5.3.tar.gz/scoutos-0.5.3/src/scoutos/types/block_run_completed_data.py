# This file was auto-generated by Fern from our API Definition.

from ..core.unchecked_base_model import UncheckedBaseModel
import typing
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class BlockRunCompletedData(UncheckedBaseModel):
    workflow_id: str
    workflow_run_id: str
    block_id: typing.Optional[str] = None
    config: typing.Dict[str, typing.Optional[typing.Any]]
    cost: typing.Optional[float] = None
    metadata: typing.Optional[typing.Dict[str, typing.Optional[typing.Any]]] = None
    state: typing.Dict[str, typing.Optional[typing.Any]]
    session_id: str
    block_type: typing.Optional[str] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
