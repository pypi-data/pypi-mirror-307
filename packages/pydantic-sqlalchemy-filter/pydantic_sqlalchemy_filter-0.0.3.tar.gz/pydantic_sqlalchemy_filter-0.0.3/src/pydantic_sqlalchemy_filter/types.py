import sqlalchemy
from sqlalchemy import Column


class DatabaseModel(sqlalchemy.orm.DeclarativeBase):
    """SQLAlchemy model.

    Fields:

        id - Primary key.

        deleted_at - Datetime when row was deleted.

    """

    id: Column
    deleted_at: Column

    def field_by_name(self, name: str) -> Column:
        """Returns sqlalchemy model Column by name."""

        raise NotImplementedError
