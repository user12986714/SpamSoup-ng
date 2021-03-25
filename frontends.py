import re


SGML_TAGS = re.compile(r'</?[^>]+>')
WORD_BOUNDARY = re.compile(r'\W*\s+\W*')

_STOPWORDS = None


def to_plain_words(post):
    plain = SGML_TAGS.sub('', post.lower())
    return WORD_BOUNDARY.split(f" {plain} ")[1:-1]


def remove_stopwords(words):
    global _STOPWORDS
    if _STOPWORDS is None:
        import nltk.corpus
        _STOPWORDS = set(nltk.corpus.stopwords.words())
    if isinstance(words, set):
        return words - _STOPWORDS
    return [w for w in words if w not in _STOPWORDS]


def tokenize_naive(post):
    return set(to_plain_words(post))


def tokenize_naive_stopwords(post):
    return remove_stopwords(set(to_plain_words(post)))


def tokenize_trigram(post):
    words = to_plain_words(post)
    if len(words) < 3:
        return ' '.join(words)
    tokens = []
    for i in range(2, len(words)):
        tokens.append(f"{words[i-2]} {words[i-1]} {words[i]}")
    return set(tokens)


def tokenize_trigram_stopwords(post):
    words = remove_stopwords(to_plain_words(post))
    if len(words) < 3:
        return ' '.join(words)
    tokens = []
    for i in range(2, len(words)):
        tokens.append(f"{words[i-2]} {words[i-1]} {words[i]}")
    return set(tokens)


__all__ = [
    'tokenize_naive', 'tokenize_naive_stopwords',
    'tokenize_trigram', 'tokenize_trigram_stopwords'
]
