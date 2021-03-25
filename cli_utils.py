import atexit
from . import database


_INIT_DB = False


def init_db(path):
    global _INIT_DB
    database.init_db(path)
    _INIT_DB = True


def close_db():
    global _INIT_DB
    if _INIT_DB:
        database.close_db()
        _INIT_DB = False


def create_table(name, silent=False):
    database.exec_sql(f"""
    CREATE TABLE {name} (
        token TEXT PRIMARY KEY,
        pos_count INTEGER NOT NULL,
        neg_count INTEGER NOT NULL
    );
    """)
    if not silent:
        print(f"Created table {name}")


def drop_table(name, silent=False):
    database.exec_sql(f"DROP TABLE {name};")
    if not silent:
        print(f"Dropped table {name}")


def vacuum(silent=False):
    database.exec_sql('VACUUM;')
    if not silent:
        print('Vacuumed the database')


atexit.register(close_db)


__all__ = ['init_db', 'close_db', 'create_table', 'drop_table', 'vacuum']
