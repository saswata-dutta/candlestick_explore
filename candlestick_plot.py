import sys
from downloader import yfinance_fetch
import candlestick_patterns
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def process(ticker, start, end):
    print(f"Downloading {ticker} between {start} and {end} ...")
    df = yfinance_fetch(ticker, start, end)
    return df


def make_vline(day):
    d = str(day)
    return dict(
        x0=d, x1=d, y0=0, y1=1, xref="x", yref="paper", line_width=15, opacity=0.15
    )


def plot(df, days, title):
    print(f"Plotting {title} ...")

    df["date_i"] = df.index
    x_axis = df["date_i"].dt.strftime("%Y-%m-%d")

    candlestick = go.Candlestick(
        x=x_axis,
        open=df["open"],
        high=df["high"],
        low=df["low"],
        close=df["close"],
        showlegend=False,
    )
    volume = go.Bar(x=x_axis, y=df["volume"], opacity=0.3, showlegend=False)

    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        subplot_titles=("OHLC", "Volume"),
        row_width=[0.2, 0.7],
    )
    fig.add_trace(candlestick, row=1, col=1)
    fig.add_trace(volume, row=2, col=1)

    fig.layout.xaxis.type = "category"
    fig.layout.xaxis2.type = "category"
    fig.update(layout_xaxis_rangeslider_visible=False)
    fig.update_layout(title=title, shapes=[make_vline(d) for d in days])

    fig.write_html(f"plot_{title}.html")


def main(ticker, start, end, patterns, condition):
    df = process(ticker, start, end)
    days = candlestick_patterns.find_days(df, patterns, condition)

    title = f"{ticker}_{start}_{end}_{'-'.join(patterns)}"
    plot(df, days, title)


if __name__ == "__main__":
    ticker, start, end, patterns, condition = sys.argv[1:]
    # ticker, start, end, patterns, condition = (
    #     "SPY",
    #     "2020-03-01",
    #     "2020-04-25",
    #     "CDLMORNINGSTAR CDLENGULFING",
    #     "CDLENGULFING > 0 or CDLMORNINGSTAR > 0",
    # )

    main(ticker, start, end, patterns.split(), condition)
