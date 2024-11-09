from .analyzer import load_sales_data, analyze_sales, save_report
import argparse


def main():
    parser = argparse.ArgumentParser(description="Analyze sales data from a CSV file.")
    parser.add_argument('--input-file', type=str, required=True, help='Input CSV file with sales data')
    parser.add_argument('--output-file', type=str, required=True, help='Output CSV file for the report')

    args = parser.parse_args()

    sales_data = load_sales_data(args.input_file)
    summary = analyze_sales(sales_data)

    save_report(summary, args.output_file)

    print(f"Отчет успешно сохранен в {args.output_file}.")
