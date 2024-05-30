from typing import Annotated

from annotated_types import Interval
from pydantic import BaseModel


class WebsiteMonitorCreate(BaseModel):
    url: str
    interval_minutes: Annotated[int, Interval(ge=1, le=90)]


class WebsiteMonitorResponse(WebsiteMonitorCreate):
    id: int