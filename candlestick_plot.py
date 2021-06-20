import sys
from downloader import yfinance_fetch
import candlestick_patterns
import plotly.graph_objects as go


def process(ticker, start, end):
    print(f"Downloading {ticker} between {start} and {end} ...")
    df = yfinance_fetch(ticker, start, end)
    return df


def make_vline(day):
    d = str(day)
    return dict(
        x0=d,
        x1=d,
        y0=0,
        y1=1,
        xref="x",
        yref="paper",
        line_width=2,
    )


def plot(df, days, title):
    print(f"Plotting {title} ...")

    df["date_str"] = df.index
    df["date_str"] = df["date_str"].dt.strftime("%Y-%m-%d")

    candlestick = go.Candlestick(
        x=df["date_str"],
        open=df["open"],
        high=df["high"],
        low=df["low"],
        close=df["close"],
    )

    fig = go.Figure(data=[candlestick])
    fig.layout.xaxis.type = "category"
    fig.update_layout(title=title, shapes=[make_vline(d) for d in days])
    fig.write_html(f"plot_{title}.html")


def main(ticker, start, end, patterns, condition):
    df = process(ticker, start, end)
    days = candlestick_patterns.find_days(df, patterns, condition)

    title = f"{ticker}_{start}_{end}_{'-'.join(patterns)}"
    plot(df, days, title)


if __name__ == "__main__":
    ticker, start, end, patterns, condition = sys.argv[1:]
    # (
    #     "SPY",
    #     "2020-03-01",
    #     "2020-04-25",
    #     "CDLMORNINGSTAR CDLENGULFING",
    #     "CDLENGULFING > 0 or CDLMORNINGSTAR > 0",
    # )
    main(ticker, start, end, patterns.split(), condition)
