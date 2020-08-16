import pandas as pd


# Utility to split the data into training and test sets.
def split_dataframe(df, holdout_fraction=0.2):
    """Splits a DataFrame into training and test sets.
    Args:
    df: a dataframe.
    holdout_fraction: fraction of dataframe rows to use in the test set.
    Returns:
    train: dataframe for training
    test: dataframe for testing
    """
    # its a random sample
    # n items o un porcentaje de datos
    test = df.sample(frac=holdout_fraction, replace=False).astype('float32')
    train = df[~df.index.isin(test.index)].astype('float32')
    return train, test
