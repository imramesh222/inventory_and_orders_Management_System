from typing import Any, List, Tuple
from sqlalchemy.orm import Query
from inventoryordersapi.domain.common import Pagination

def paginate_query(query: Query, limit: int = 100, offset: int = 0, page: int = 1, page_size: int = 10) -> Tuple[List[Any], Pagination]:
    """
    Paginate a SQLAlchemy query and return results + pagination info.
    """
    total_count = query.count()
    results = query.offset(offset).limit(limit).all()

    next_cursor = str(offset + limit) if offset + limit < total_count else None
    prev_cursor = str(max(offset - limit, 0)) if offset > 0 else None

    pagination = Pagination(
        total=total_count,
        page=page,
        page_size=page_size,
        next_cursor=next_cursor,
        prev_cursor=prev_cursor
    )

    return results, pagination
