from mlxtend.preprocessing import TransactionEncoder
import pandas as pd


def mlxtend_encode(dataset):
    te = TransactionEncoder()
    te_ary = te.fit(dataset).transform(dataset)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    return df

