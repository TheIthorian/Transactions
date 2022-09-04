from transactions.models import Tag

# https://docs.pytest.org/en/7.1.x/getting-started.html#get-started
def test_Tag():
    assert str(Tag("A", "B", "C")) == "<Tag L1: A, L2: B, L3: C>"
