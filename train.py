from . import database


def batch_train(data, frontend, table, meta_token):
    tokens = {}
    meta = [0, 0]
    for post, is_pos in data:
        for token in frontend(post):
            if token not in tokens:
                tokens[token] = [0, 0]
            tokens[token][is_pos] += 1
        meta[is_pos] += 1
    database.exec_sql('BEGIN TRANSACTION;')
    upsert_sql = f"""
    INSERT INTO {table} (token, pos_count, neg_count)
    VALUES (?, ?, ?)
    ON CONFLICT (token) DO UPDATE SET
        pos_count = pos_count + excluded.pos_count,
        neg_count = neg_count + excluded.neg_count
    WHERE token = excluded.token;
    """
    for token in tokens:
        pos_count = tokens[token][True]
        neg_count = tokens[token][False]
        if pos_count + neg_count > 5:
            database.exec_sql(upsert_sql, [token, pos_count, neg_count])
    pos_count = meta[True]
    neg_count = meta[False]
    database.exec_sql(upsert_sql, [meta_token, pos_count, neg_count])
    database.exec_sql('COMMIT;')


__all__ = ['batch_train']
