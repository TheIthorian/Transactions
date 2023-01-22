from app.importer.reader import Reader


class Register:
    readers: list[Reader]

    def __init__(self):
        self.readers = []

    def add(self, reader: Reader):
        self.readers.append(reader)

    def get_sources(self) -> list[str]:
        return [reader.source for reader in self.readers]

    def get_reader(self, source: str) -> Reader:
        reader = None
        for r in self.readers:
            if r.source == source:
                reader = r

        return reader
