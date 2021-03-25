import sqlite3


_CON = None
_CUR = None


def init_db(path):
    global _CON, _CUR
    _CON = sqlite3.connect(path, isolation_level=None)
    _CUR = _CON.cursor()


def close_db():
    global _CON, _CUR
    _CUR.close()
    _CON.close()
    _CUR = None
    _CON = None


def fetch_stat(table, meta_token='<meta>'):
    _CUR.execute(f"""
    SELECT pos_count, neg_count
    FROM {table}
    WHERE token = ?
    """, [meta_token])
    return _CUR.fetchall()[0]


def fetch_data(tokens, table):
    placeholders = ', '.join(['?' for _ in tokens])
    _CUR.execute(f"""
    SELECT pos_count, neg_count
    FROM {table}
    WHERE token IN ({placeholders});
    """, list(tokens))
    return _CUR.fetchall()


__all__ = ['init_db', 'close_db', 'fetch_stat', 'fetch_data']
