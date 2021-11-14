import sqlite3
from dataclasses import astuple

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor, execute_batch

from sqlite_to_postgres.models import Person, Genre, FilmWork, PersonFilmWork, GenreFilmWork


class SQLiteLoader:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def load(self, table, dataclass):
        batch = []
        for row in self.cursor.execute(f'select * from {table}'):
            batch.append(dataclass(*row))
            if len(batch) == 500:
                yield batch
                batch.clear()

        yield batch
        batch.clear()


class PostgresSaver:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def save(self, batch, table):
        values = [astuple(row) for row in batch]
        table_name = sql.Identifier(table)
        col_names = ', '.join(batch[0].__dict__.keys())
        placeholders = ',%s ' * len(values[0])
        query = sql.SQL("INSERT INTO {table} ({col_names}) VALUES ({values});".format(
            table=table_name.string,
            col_names=col_names,
            values=placeholders[1:]
        ))
        execute_batch(self.cursor, query, values)


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_loader = SQLiteLoader(connection)
    postgres_saver.connection.autocommit = True

    table_dataclass_mapping = {
        'person': Person,
        'genre': Genre,
        'film_work': FilmWork,
        'person_film_work': PersonFilmWork,
        'genre_film_work': GenreFilmWork
    }

    for table, dataclass in table_dataclass_mapping.items():
        for batch in sqlite_loader.load(table, dataclass):
            postgres_saver.save(batch, table)

    sqlite_loader.cursor.close()


if __name__ == '__main__':
    dsl = {
        'dbname': 'cinema',
        'user': 'cinema',
        'password': 'cinema',
        'host': '127.0.0.1',
        'port': 14001,
        'options': '-c search_path=content',
    }
    with sqlite3.connect('slack.sqlite') as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)

    sqlite_conn.close()
