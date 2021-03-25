import database
import bayes


FRONTENDS = []


def use_frontend(frontend, table, pos_acc, neg_acc,
                 meta_token='<meta>', prior=None):
    FRONTENDS.append((frontend, table, meta_token, pos_acc, neg_acc, prior))


def classify(post):
    total_score = 0
    for frontend, table, meta_token, pos_acc, neg_acc, prior in FRONTENDS:
        tokens = frontend(post)
        stat = database.fetch_stat(table, meta_token)
        data = database.fetch_data(table, tokens)
        pos_all, neg_all = stat
        if prior is None:
            prior = pos_all / (pos_all + neg_all)
        score = bayes.calculate_score(data, pos_all, neg_all, prior)
        balanced = score - 0.5
        refined = balanced * (abs(balanced) / 0.5) * 200
        total_score += refined * (pos_acc if refined > 0 else neg_acc)
    return total_score


__all__ = ['FRONTENDS', 'use_frontend', 'classify']
