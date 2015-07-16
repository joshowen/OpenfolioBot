from datetime import datetime
import praw
from yahoo_finance import Share

CONFIG = {}
REDIRECT_URI = "http://www.openfolio.com"
SUBREDDIT = "oftestsandbox"
USER_AGENT = "OpenfolioTest 0.1"

def run(reddit_obj, tickers):
    subreddit = reddit_obj.get_subreddit(SUBREDDIT)

    for submission in subreddit.get_new():
        parsed_tickers = parse_tickers(submission.title) & tickers
        if parsed_tickers:
            #print(generate_comment(parsed_tickers))
            submission.reply(generate_comment(parsed_tickers))
        
    for comment in subreddit.get_comments():
        parsed_tickers = parse_tickers(comment.body) & tickers
        if parsed_tickers:
            #print(generate_comment(parsed_tickers))
            comment.reply(generate_comment(parsed_tickers))


def generate_comment(tickers):
    """
    Generate text for a comment given the ticker names
    """
    for ticker in sorted(tickers):
        stk = Share(ticker)
        now = datetime.now()
        return '''
        ### {}\n
        =======\n
        * Price: {}
        * Market Cap: {}\n
        ######*as of {} via [Openfolio](http://www.openfolio.com)*
        '''.format(ticker.upper(), stk.get_price(), stk.get_market_cap(), 
                   now.strftime('%Y/%m/%d %H:%M:%S'))


def parse_tickers(text):
    """
    Finds any 3+ letter uppercase word and returns a set of them
    """
    return set((s for s in text.split(' ') if len(s) >= 3 and s.isupper()))


def init_reddit():
    p = praw.Reddit(user_agent=USER_AGENT)
    p.set_oauth_app_info(CONFIG['CLIENT_ID'], CONFIG['CLIENT_SECRET'], REDIRECT_URI)
    p.set_access_credentials(**p.refresh_access_information(CONFIG['REFRESH_TOKEN']))
    assert p.is_oauth_session()
    return p


if __name__ == "__main__":
    with open('tickers.txt') as ticker_buffer:
        tickers = set(line.split(' ')[0] for line in ticker_buffer.readlines() if line)
    with open('config.txt') as config:
        for line in config.readlines():
            key, val = tuple(line.strip().split(': '))
            CONFIG[key] = val

    run(init_reddit(), tickers)
