from constants import SUPPORTED_TICKERS
from yahoo_finance import Share

PUNCTUATION = set(".;:-,!@#$&*()[]{}?/\\%^<>=+'")


def to_tokens(comment):
    comment = ''.join(ch for ch in comment if ch not in PUNCTUATION)
    return comment.split(' ')


def find_tickers(tokens):
    possible_tickers = set((s for s in tokens if len(s) >= 3 and s.isupper()))
    return possible_tickers & SUPPORTED_TICKERS.viewkeys()


def render_comment(tickers):
    for ticker in sorted(tickers):
        stk = Share(ticker)
        print '''%s trading at %s.''' % (ticker.upper(), stk.get_price())
