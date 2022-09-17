class QueryBuilder:
    _existing_query: str
    _select: list[str]
    _conditions: list[str]
    _group_by: list[str]
    _order_by: list[str]
    _inputs: list[str]

    def __init__(self, existing_query: str = None, existing_inputs: list[str] = []):
        self._existing_query = existing_query
        self._select = []
        self._conditions = []
        self._group_by = []
        self._order_by = []
        self._inputs = existing_inputs.copy()

    def select(self, columns: list[str]) -> "QueryBuilder":
        for column in columns:
            self._select.append(column)
        return self

    def order_by(self, order_list: list[str]) -> "QueryBuilder":
        self._order_by.extend(order_list)
        return self

    def add_input(self, val) -> "QueryBuilder":
        if type(val) is list:
            self._inputs.extend(val)
        else:
            self._inputs.append(val)
        return self

    def get_inputs(self) -> list:
        return self._inputs

    def build(self) -> str:
        query = ""
        if self._existing_query is not None:
            query = self._existing_query

        query = self.build_select(query)
        query = self.build_conditions(query)
        query = self.build_order_by(query)

        return query

    def build_select(self, query: str) -> str:
        query += ", ".join(self._select)
        return query

    def build_conditions(self, query: str) -> str:
        if len(self._conditions) != 0:
            query += " WHERE " + " AND ".join(self._conditions)
        return query

    def build_order_by(self, query: str) -> str:
        if len(self._order_by) != 0:
            query += " ORDER BY " + ", ".join(self._order_by)
        return query
