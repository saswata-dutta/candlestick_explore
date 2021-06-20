from talib import abstract

PATTERNS = ["CDLMARUBOZU", "CDLENGULFING", "CDLMORNINGSTAR"]
# talib.get_function_groups()['Pattern Recognition']


def detect(df):
    for pattern in PATTERNS:
        print(f"Pattern {pattern} ...")
        df[pattern] = abstract.Function(pattern)(df)

    return df


def find_days(df, patterns, condition):
    for pattern in patterns:
        df[pattern] = abstract.Function(pattern)(df)

    days = (d.date() for d in df.query(condition).index)
    return days
