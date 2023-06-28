import sqlite3
import typing
import uuid
from abc import ABC, abstractmethod
from menubar_dataclasses import Todo, Preference

class TodoRepo():

    def __init__(self,  location: str, engine: typing.Literal['sqlite', 'txt'] = 'sqlite'):
        self.location = location
        match engine:
            case "sqlite":
                self.engine = SqliteEngine(location = self.location)

    def save_all_todo(self, todos: list[Todo]):
        self.engine.save_all_todo(todos)

    def get_all_todo(self) -> list[Todo]:
        return self.engine.get_all_todo()

class TodoEngine(ABC):

    @abstractmethod
    def save_all_todo(self, todos: list[Todo]):
        ...

    @abstractmethod
    def get_all_todo(self) -> list[Todo]:
        ...


class SqliteEngine(TodoEngine):
    _TODO_TABLE_NAME = "todo"
    _TODO_SCHEMA = f"""CREATE TABLE 
            IF NOT EXISTS {_TODO_TABLE_NAME}
            (
                uuid UUID,
                description text not null,
                current_status text text not null,
                created_on timestamp not null default current,
                completed_on timestamp
            );"""

    _PREF_TABLE_NAME = "preferences"
    _PREF_SCHEMA = f"""CREATE TABLE
            IF NOT EXISTS {_PREF_TABLE_NAME}
            (
                pref_name text not null,
                pref_value text not null,
                updated_on timestamp not null default current
            );"""

    def __init__(self, location: str, DEBUG=False):
        self.DEBUG = DEBUG
        self.db_name = f"{location}/menubar_todo.db"
        self._conn = sqlite3.connect(self.db_name, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        sqlite3.register_adapter(uuid.UUID, lambda u: u.bytes_le)
        sqlite3.register_converter('uuid', lambda b: uuid.UUID(bytes_le=b))

        try:
            with self._conn:
                script = self._TODO_SCHEMA if not DEBUG else f"DROP table if exists {self._TODO_TABLE_NAME}; {self._TODO_SCHEMA}"
                script += self._PREF_SCHEMA if not DEBUG else f"DROP table if exists {self._PREF_TABLE_NAME}; {self._PREF_SCHEMA}"
                print(script) if DEBUG else ...
                self._conn.executescript(script)
                self._conn.commit()
                self.print_todo_schema() if DEBUG else ...
                self.print_pref_schema() if DEBUG else ...
        except sqlite3.Error as e:
            print(f"SQLite error on table create: {e}")

    def print_pref_schema(self) -> None:
        try:
            with self._conn:
                print("(cid, name, type, notnull, dflt_value, pk)")
                for row in self._conn.execute(f"PRAGMA table_info('{self._PREF_TABLE_NAME}')").fetchall():
                    print(row)
        except sqlite3.Error as e:
            print(f"{self._PREF_TABLE_NAME} schema does not exist")

    def print_todo_schema(self) -> None:
        try:
            with self._conn:
                print("(cid, name, type, notnull, dflt_value, pk)")
                for row in self._conn.execute(f"PRAGMA table_info('{self._TODO_TABLE_NAME}')").fetchall():
                    print(row)
        except sqlite3.Error as e:
            print(f"{self._TODO_TABLE_NAME} schema does not exist")

    def get_all_todo(self) -> list[Todo]:
        script = "SELECT * FROM Todo;"
        resp = self._conn.executescript(script)
        return [self._sql_to_todo_mapper(row) for row in resp.fetchall()]

    def _sql_to_todo_mapper(self, todo_sql: tuple) -> Todo:
        return Todo(*todo_sql)

    def save_all_todo(self, todos: list[Todo]) -> None:
        script = ""