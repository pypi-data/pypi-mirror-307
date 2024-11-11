from pathlib import Path
from typing import Annotated

import lox_space as lox
import pydantic
from pydantic import Field

from ephemerista.form_widget import FormWidgetHandler


class BaseModel(FormWidgetHandler, pydantic.BaseModel):
    def __init__(self, **data):
        pydantic.BaseModel.__init__(self, **data)
        FormWidgetHandler.__init__(self)


UT1Provider = lox.UT1Provider

_UT1_PROVIDER: UT1Provider | None = None


def init_provider(eop_file: str | Path):
    if isinstance(eop_file, Path):
        eop_file = str(eop_file)
    global _UT1_PROVIDER  # noqa: PLW0603
    _UT1_PROVIDER = lox.UT1Provider(eop_file)


def get_provider() -> UT1Provider:
    if _UT1_PROVIDER is None:
        msg = "UT1 provider not initialized. Call `init_provider` first."
        raise ValueError(msg)
    return _UT1_PROVIDER


def annotate_vec3_field(s):
    # Assumes there's only one vec3 per form
    s["$id"] = "/schemas/vec3"


Vec3: type = Annotated[
    tuple[float, float, float],
    Field(..., json_schema_extra=annotate_vec3_field),
]  # type: ignore
