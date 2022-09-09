# https://docs.pytest.org/en/7.1.x/getting-started.html#get-started
from app.transactions.transaction_schema import Tag


def test_Tag():
    assert str(Tag("A", "B", "C")) == "<Tag l1: A, l2: B, l3: C>"
