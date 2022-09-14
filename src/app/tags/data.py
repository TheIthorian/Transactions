from functools import lru_cache

from app.tags.tag_model import Tag
from app import database


@lru_cache(1)
def get_all_tags() -> list[Tag]:
    """Finds all unique tags in used by any transaction."""
    result = database.select(
        "SELECT DISTINCT l1, l2, l3 FROM Transactions ORDER BY l1, l2, l3"
    )

    return [Tag(l1=row[0], l2=row[1], l3=row[2]) for row in result]
