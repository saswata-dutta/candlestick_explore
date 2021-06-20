import sys
import pandas as pd
from downloader import yfinance_fetch
import candlestick_patterns


TICKER_SUFFIX = ".NS"


def process(ticker, start, end):
    print(f"Downloading {ticker} ...")
    df = yfinance_fetch(ticker, start, end)

    print(f"Processing {ticker} ...")
    df = candlestick_patterns.detect(df)
    return df


def main(company_file, start, end):
    companies = pd.read_csv(company_file)

    companies_data = []
    for symbol, industry in zip(companies["SYMBOL"], companies["INDUSTRY"]):
        try:
            df = process(symbol + TICKER_SUFFIX, start, end)
        except Exception as e:
            print(f"Failed to process {symbol} !")
            print(e)
        else:
            df["symbol"] = symbol
            df["industry"] = industry
            companies_data.append(df)

    report = pd.concat(companies_data)
    report.to_csv(f"report_{start}_{end}.csv")


if __name__ == "__main__":
    company_file, start, end = sys.argv[1:]
    main(company_file, start, end)
