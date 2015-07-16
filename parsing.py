from constants import SUPPORTED_TICKERS
from yahoo_finance import Share
from datetime import datetime

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
        now = datetime.now()
        print '''### %s\n
=======\n
* Price: %s
* Market Cap: %s\n
######*as of %s via [Openfolio](http://www.openfolio.com)*
            
            ''' % (ticker.upper(), stk.get_price(), stk.get_market_cap(), now.strftime('%Y/%m/%d %H:%M:%S'))
