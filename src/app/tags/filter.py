from app.tags.tag_model import Tag


def filter_tags_by_l1(tags: list[Tag], l1_value: str):
    return list(filter(lambda t: t.l1 == l1_value, tags))


def filter_tags_by_l2(tags: list[Tag], l2_value: str):
    return list(filter(lambda t: t.l2 == l2_value, tags))


def filter_tags_by_l3(tags: list[Tag], l3_value: str):
    return list(filter(lambda t: t.l3 == l3_value, tags))
