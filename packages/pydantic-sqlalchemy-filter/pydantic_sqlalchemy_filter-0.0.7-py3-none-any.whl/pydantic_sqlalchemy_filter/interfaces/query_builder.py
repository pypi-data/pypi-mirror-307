import abc

from sqlalchemy import Select

from pydantic_sqlalchemy_filter.types import DatabaseModel


class IQueryBuilder(abc.ABC):
    """Query builder Protocol."""

    @abc.abstractmethod
    def build_count_query(
        self,
        model: DatabaseModel,
        exclude_deleted: bool,
        query: Select | None = None,
    ) -> Select:
        raise NotImplementedError

    @abc.abstractmethod
    def build_select_query(
        self,
        model: DatabaseModel,
        exclude_deleted: bool,
        query: Select | None = None,
    ) -> Select:
        raise NotImplementedError

    @abc.abstractmethod
    def build_base_query(
        self,
        model: DatabaseModel,
        exclude_deleted: bool,
    ) -> Select:
        raise NotImplementedError

    @abc.abstractmethod
    def _filter(
        self,
        model: DatabaseModel,
        exclude_deleted: bool,
        query: Select | None = None,
    ) -> Select:
        raise NotImplementedError

    @abc.abstractmethod
    def _sort(
        self,
        query: Select,
        model: DatabaseModel,
        with_collate: str = None,
    ) -> Select:
        raise NotImplementedError

    @abc.abstractmethod
    def _paginate(
        self,
        query: Select,
    ) -> Select:
        raise NotImplementedError

    @abc.abstractmethod
    def _sort_subquery(
        self,
        subquery: Select,
    ) -> Select:
        raise NotImplementedError
