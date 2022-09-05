from transactions.models.transactions import Tag

# https://docs.pytest.org/en/7.1.x/getting-started.html#get-started
def test_Tag():
    assert str(Tag("A", "B", "C")) == "<Tag l1: A, l2: B, l3: C>"
