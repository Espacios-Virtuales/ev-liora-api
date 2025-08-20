# app/utils/pagination.py
from math import ceil

def paginate_query(query, page: int, page_size: int):
    """Devuelve (items, meta) para SQLAlchemy query."""
    page = max(page or 1, 1)
    page_size = min(max(page_size or 20, 1), 200)

    total = query.order_by(None).count()
    total_pages = max(ceil(total / page_size), 1)
    page = min(page, total_pages)

    items = query.limit(page_size).offset((page - 1) * page_size).all()

    meta = {
        "total": total,
        "total_pages": total_pages,
        "first_page": 1,
        "last_page": total_pages,
        "page": page,
        "previous_page": page - 1 if page > 1 else None,
        "next_page": page + 1 if page < total_pages else None,
    }
    return items, meta
