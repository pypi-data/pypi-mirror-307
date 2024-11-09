import pandas as pd


def load_sales_data(file_path):
    return pd.read_csv(file_path)


def analyze_sales(sales_data):
    summary = sales_data.groupby('category').agg(
        sales=('amount', 'sum'),
        quantity=('quantity', 'sum')
    ).reset_index()
    return summary


def save_report(summary, output_file):
    summary.to_csv(output_file, index=False)
