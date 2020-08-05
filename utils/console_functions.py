def print_debug(label, data):
    print(label+": \n", data, end='\n\n')


def get_summary_df(df_label, df):
    print_debug(df_label + ".head()", df.head())
    print_debug(df_label + ".columns", df.columns)
    print_debug(df_label + ".iloc[0]", df.iloc[0])
    print_debug(df_label + ".describe()", df.describe())

