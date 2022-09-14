from dataclasses import asdict, dataclass


TAG_COLOR_MAP = {
    "Insurance": "orange",
    "Transfers": "cyan",
    "Appearance": "cyan",
    "Bills": "green",
    "Unknown": "gray",
    "Transport": "blue",
    "Family": "purple",
    "Enjoyment": "magenta",
    "Home": "green",
    "Savings": "magenta",
    "Repayments": "cyan",
    "One-off or Other": "geekblue",
    "Income": "lime",
}


@dataclass
class Tag:
    """In moneydashboard, a transaction can have up to 3 levels of tags. Increasing levels are more specific."""

    l1: str
    l2: str
    l3: str
    color: str = None

    def __init__(self, l1, l2, l3):
        self.l1 = l1
        self.l2 = l2
        self.l3 = l3
        self.color = TAG_COLOR_MAP[self.l1] if self.l1 in TAG_COLOR_MAP else None

    def __eq__(self, other: "Tag"):
        return self.l1 == other.l1 and self.l2 == other.l2 and self.l3 == other.l3

    def to_dict(self):
        return asdict(self)

    def is_in(self, other_tags: list) -> bool:
        """Returns True if the current tag is in a lsit of `other_tags`."""
        for tag in other_tags:
            if self == tag:
                return True
        return False


@dataclass
class TagLists:
    """Datastructure to store lists of tags, separated by tag level."""

    l1: list[str] = None
    l2: list[str] = None
    l3: list[str] = None
