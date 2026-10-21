from datetime import UTC, datetime

from sqlmodel import Field, Relationship, SQLModel


def now_utc() -> datetime:
    return datetime.now(UTC)


class Url(SQLModel, table=True):
    __tablename__ = "urls"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=255, unique=True, index=True)
    created_at: datetime = Field(default_factory=now_utc)

    checks: list["UrlCheck"] = Relationship(
        back_populates="url",
        sa_relationship_kwargs={
            "order_by": "UrlCheck.id.desc()",
            "lazy": "selectin",
        },
    )


class UrlCheck(SQLModel, table=True):
    __tablename__ = "url_checks"

    id: int | None = Field(default=None, primary_key=True)
    url_id: int = Field(foreign_key="urls.id", index=True)
    status_code: int | None = None
    h1: str | None = Field(default=None, max_length=255)
    title: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    created_at: datetime = Field(default_factory=now_utc)

    url: Url | None = Relationship(back_populates="checks")
