from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.testing.schema import mapped_column


class Base(DeclarativeBase):
    pass


class UsersTable(Base):
    __tablename__ = 'users_table'
    id: Mapped[int] = mapped_column(primary_key=True)
    api_key: Mapped[str] = mapped_column(nullable=True)


def create_database(path: str):
    engine = create_engine("sqlite:///" + path)
    Base.metadata.create_all(engine)