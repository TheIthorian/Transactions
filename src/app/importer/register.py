from app.importer.reader import Reader
from app.importer import md_reader, metro_reader


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


def register_readers() -> Register:
    register = Register()
    register.add(md_reader.md_reader())
    register.add(metro_reader.metro_reader())

    return register
