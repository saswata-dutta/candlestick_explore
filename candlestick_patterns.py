from talib import abstract

PATTERNS = ["CDLMARUBOZU", "CDLENGULFING", "CDLMORNINGSTAR"]
# talib.get_function_groups()['Pattern Recognition']


def detect(df):
    for pattern in PATTERNS:
        print(f"Pattern {pattern} ...")
        df[pattern] = abstract.Function(pattern)(df)

    return df


def find_days(df, pattern, condition):
    df[pattern] = abstract.Function(pattern)(df)
    days = (d.date() for d in df.query(condition).index)
    return days
