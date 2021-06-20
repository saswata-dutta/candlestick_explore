import yfinance as yf


def normalise_name(s):
    return s.replace(" ", "_").lower()


def normalise(df):
    df.columns = [normalise_name(c) for c in df.columns]
    df.index.names = [normalise_name(c) for c in df.index.names]
    return df.round(2)


def yfinance_fetch(ticker, start, end):
    df = yf.download(ticker, group_by="Ticker", start=start, end=end)
    return normalise(df)
