from app.transactions.breakdown import (
    get_transaction_amounts_by_tag_level,
)


class Test_get_breakdown_by_tag:
    def test_returns_grouped_l1_tags(self, mocker):
        # given
        mock_query_results = [
            [20_000, "Income"],
            [-15_000, "Home"],
            [-7_000, "Appearance"],
            [-2_000, "Enjoyment"],
        ]

        mocker.patch("app.database.select", return_value=mock_query_results)

        result = get_transaction_amounts_by_tag_level(1)

        assert result == [
            ("Income", 20_000),
            ("Home", -15_000),
            ("Appearance", -7_000),
            ("Enjoyment", -2_000),
        ]

    def test_returns_grouped_l2_tags(self, mocker):
        # given
        mock_query_results = [
            [20_000, "Income", ""],
            [-10_000, "Home", "Bills"],
            [-5_000, "Home", "Other"],
            [-7_000, "Appearance", "Clothes"],
            [-2_000, "Enjoyment", "Eating Out"],
        ]

        mocker.patch("app.database.select", return_value=mock_query_results)

        result = get_transaction_amounts_by_tag_level(2)

        assert result == [
            ("", 20_000),
            ("Bills", -10_000),
            ("Other", -5_000),
            ("Clothes", -7_000),
            ("Eating Out", -2_000),
        ]

    def test_returns_grouped_l3_tags(self, mocker):
        # given
        mock_query_results = [
            [20_000, "Income", "", ""],
            [-10_000, "Home", "Bills", ""],
            [-5_000, "Home", "Other", ""],
            [-4_000, "Appearance", "Clothes", "Everyday"],
            [-3_000, "Appearance", "Clothes", "Work"],
            [-2_000, "Enjoyment", "Eating Out", "Everyday"],
        ]

        mocker.patch("app.database.select", return_value=mock_query_results)

        result = get_transaction_amounts_by_tag_level(3)

        assert result == [
            ("", 20_000),
            ("", -10_000),
            ("", -5_000),
            ("Everyday", -4_000),
            ("Work", -3_000),
            ("Everyday", -2_000),
        ]
