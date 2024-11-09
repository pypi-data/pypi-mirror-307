import pandas as pd


def load_transactions(file_path):
    return pd.read_csv(file_path)


def summarize_transactions(transactions):
    summary = transactions.groupby('category')['amount'].sum().to_dict()
    return summary
