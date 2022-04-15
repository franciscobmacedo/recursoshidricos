import datetime
from typing import Any, List

from django.db.models import QuerySet
from ninja import Schema
from ninja.conf import settings
from ninja.pagination import PaginationBase
from ninja.types import DictStrAny
from pydantic import Field


class ParametersFilter(Schema):
    station_uids: List[str] = Field(None, alias="station_uids")


class DataBounds(Schema):
    station_uids: List[str]
    parameter_uids: List[str]


class DataFilter(DataBounds):
    tmin: datetime.date = Field("1950-01-01")
    tmax: datetime.date = Field(datetime.date.today().strftime("%Y-%m-%d"))


class Pagination(PaginationBase):
    class Input(Schema):
        page_size: int = Field(settings.PAGINATION_PER_PAGE, gt=0)
        page: int = Field(1, gt=0)

    class Output(Schema):
        total_pages: int
        page: int
        per_page: int
        count: int
        items: List[Any]

    def _total_pages(self, queryset: QuerySet, page_size: int) -> int:
        return max(int(self._items_count(queryset) / page_size), 1)

    def paginate_queryset(
        self,
        queryset: QuerySet,
        pagination: Input,
        **params: DictStrAny,
    ) -> Any:
        offset = (pagination.page - 1) * pagination.page_size
        print(params)
        return {
            "total_pages": self._total_pages(queryset, pagination.page_size),
            "page": pagination.page,
            "per_page": pagination.page_size,
            "count": self._items_count(queryset),
            "items": queryset[offset : offset + pagination.page_size],
        }
