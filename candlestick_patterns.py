from talib import abstract

PATTERNS = ["CDLMARUBOZU", "CDLENGULFING", "CDLMORNINGSTAR"]
# talib.get_function_groups()['Pattern Recognition']


def detect(df):
    for pattern in PATTERNS:
        df[pattern] = abstract.Function(pattern)(df)

    return df
