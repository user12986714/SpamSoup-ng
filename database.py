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


def exec_sql(sql, params=None):
    _CUR.execute(sql, params)
    return _CUR.fetchall()


def fetch_stat(table, meta_token='<meta>'):
    return exec_sql(f"""
    SELECT pos_count, neg_count
    FROM {table}
    WHERE token = ?
    """, [meta_token])[0]


def fetch_data(table, tokens):
    placeholders = ', '.join(['?' for _ in tokens])
    return exec_sql(f"""
    SELECT pos_count, neg_count
    FROM {table}
    WHERE token IN ({placeholders});
    """, list(tokens))


__all__ = ['exec_sql', 'init_db', 'close_db', 'fetch_stat', 'fetch_data']
