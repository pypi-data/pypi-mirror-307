
def dfunique(df, dropna=True):
    '''
    Method to get unique values and their corresponding counts per column in
    a dataframe.

    df.unique() function only returns unique values per df series.
    df.nunique() function returns number of unique values by col (default axis=0),
    e.g., nunique(axis=0, dropna=True).

    Parameters
    ----------
    df              : pandas.core.frame.DataFrame
        Pandas dataframe that represents the original input.
    dropna          : boolean (default=True)
        Whether null values are to be dropped.

    Returns
    -------
    uniq_ls         : list, unique values per col.
    cntr_ls         : list, count of unique values per col.
    '''

    cols    = df.columns.tolist()
    uniq_ls = []
    cntr_ls = []
    for c in cols:
        if dropna is True:
            uniqval = df[f'{c}'].dropna().unique()
            uniq_ls.append(uniqval)
            cntr_ls.append(len(uniqval) )
        else:
            uniqval = df[f'{c}'].unique()
            uniq_ls.append(uniqval)
            cntr_ls.append(len(uniqval) )

    return uniq_ls, cntr_ls
