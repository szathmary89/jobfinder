
from datetime import datetime

from sqlalchemy import String, Text, Integer, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    company: Mapped[str] = mapped_column(String(255), nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)

    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    salary_min: Mapped[int | None] = mapped_column(Integer, nullable=True)
    salary_max: Mapped[int | None] = mapped_column(Integer, nullable=True)
    salary_currency: Mapped[str] = mapped_column(
        String(3), default="HUF"
    )

    employment_type: Mapped[str | None] = mapped_column(
        String(50), nullable=True
    )
    work_schedule: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )
    remote_type: Mapped[str | None] = mapped_column(
        String(50), nullable=True
    )

    source: Mapped[str] = mapped_column(String(100), nullable=False)
    source_url: Mapped[str] = mapped_column(
        String(1000), nullable=False
    )

    published_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True
    )
    collected_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True
    )
