# Python
from typing import TypeVar, TypedDict, Optional

# Django
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.manager import BaseManager


_Z = TypeVar("_Z")


class PaginateType(TypedDict):
    limit: int
    page: int
    startIndex: int
    hasNext: bool
    sort: Optional[str]
    total: int
    totalPage: int


def paginate(entries: BaseManager[_Z], page_number: int, limit: int, sort: str | None) -> tuple[BaseManager[_Z], PaginateType]: # type: ignore
    paginator = Paginator(entries, limit)

    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
        
    pd: PaginateType = {
        "limit": limit,
        "page": page_number,
        "startIndex": page.start_index(),
        "hasNext": page.has_next(),
        "sort": sort,
        "total": paginator.count,
        "totalPage": paginator.num_pages,
    }

    return page.object_list, pd # type: ignore