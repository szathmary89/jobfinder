
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class JobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    company: str
    location: str
    description: str | None = None

    salary_min: int | None = None
    salary_max: int | None = None
    salary_currency: str

    employment_type: str | None = None
    work_schedule: str | None = None
    remote_type: str | None = None

    source: str
    source_url: str

    published_at: datetime | None = None
    collected_at: datetime
    is_active: bool
