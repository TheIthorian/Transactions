from app.util.list import unique


class Test_unique:
    def test_returns_unique_list_of_numbers(self):
        # Given
        numbers = [1, 2, 3, 4, 4, 5, 6, 1]

        # When
        result = unique(numbers)

        # Then
        assert result == [1, 2, 3, 4, 5, 6]

    def test_returns_unique_list_of_hashables(self):
        # Given
        hashables = [{1, 2}, {1, 2}, {}, {1}, {1, 2, 3}, {"string"}, {"string"}]

        # When
        result = unique(hashables)

        # Then
        assert result == [{1, 2}, {}, {1}, {1, 2, 3}, {"string"}]
