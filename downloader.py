import yfinance as yf
from retrying import retry


def normalise_name(s):
    return s.replace(" ", "_").lower()


def normalise(df):
    df.columns = [normalise_name(c) for c in df.columns]
    df.index.names = [normalise_name(c) for c in df.index.names]
    return df.round(2)


@retry(
    stop_max_attempt_number=5,
    wait_exponential_multiplier=200,
    wait_exponential_max=10000,
)
def yfinance_fetch(ticker, start, end):
    df = yf.download(ticker, group_by="Ticker", start=start, end=end)
    assert len(df) > 0, f"Empty response {ticker} between {start} {end} !"
    return normalise(df)
