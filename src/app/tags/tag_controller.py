from app.http.request import Request
from app.tags.tag_model import Tag
from app.tags import data


def get_all_tags(request: Request = None) -> list[Tag]:
    # print(data.get_all_tags.cache_info())
    return data.get_all_tags()
