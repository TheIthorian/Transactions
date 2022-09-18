from app.tags.tag_model import Tag


class Test_Tag:
    def test_assigns_correct_color(self):
        # Given / When
        tag = Tag(l1="Income")

        # Then
        assert tag.color == "lime"

    def test_assigns_correct_defaults(self):
        # Given / When
        tag = Tag(l1="Income")

        # Then
        assert tag.l2 == ""
        assert tag.l3 == ""

    class Test_equality:
        def test_same_tags_return_true(self):
            tag1 = Tag(l1="A", l2="B", l3="C")
            tag2 = Tag(l1="A", l2="B", l3="C")
            tag2.color = "lime"

            assert tag1 == tag2

        def test_different_tags_return_false(self):
            tag1 = Tag(l1="A", l2="B", l3="C")
            tag2 = Tag(l1="A", l2="B", l3="X")
            tag3 = Tag(l1="A", l2="X", l3="C")
            tag4 = Tag(l1="X", l2="B", l3="C")

            assert tag1 != tag2
            assert tag1 != tag3
            assert tag1 != tag4

    def test_to_dict_returns_correct_dict(self):
        tag = Tag(l1="A", l2="B", l3="C")
        tag.color = "lime"

        assert tag.to_dict() == {"l1": "A", "l2": "B", "l3": "C", "color": "lime"}

    class Test_is_in:
        def test_is_in_returns_true_when_list_constains_tag(self):
            # Given
            tag_list: list[Tag] = [
                Tag(l1="A", l2="B", l3="C"),
                Tag(l1="A", l2="B", l3="X"),
                Tag(l1="A", l2="X", l3="C"),
                Tag(l1="X", l2="B", l3="C"),
            ]

            # When / Then
            assert Tag(l1="A", l2="B", l3="C").is_in(tag_list)
            assert not Tag(l1="X", l2="B", l3="X").is_in(tag_list)
