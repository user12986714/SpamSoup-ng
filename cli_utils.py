import atexit
import database


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


def create_table(name):
    database.exec_sql(f"""
    CREATE TABLE {name} (
        token TEXT PRIMARY KEY,
        pos_count INTEGER NOT NULL,
        neg_count INTEGER NOT NULL
    );
    """)


def drop_table(name):
    database.exec_sql(f"DROP TABLE {name};")


def vacuum():
    database.exec_sql('VACUUM;')


atexit.register(close_db)


__all__ = ['init_db', 'close_db', 'create_table', 'drop_table', 'vacuum']
