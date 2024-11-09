from .analyzer import load_transactions, summarize_transactions
import argparse


def main():
    parser = argparse.ArgumentParser(description="Analyze transactions from a CSV file.")
    parser.add_argument('--input-file', type=str, required=True, help='Input CSV file with transactions')
    parser.add_argument('--output-file', type=str, required=True, help='Output TXT file for the report')

    args = parser.parse_args()

    transactions = load_transactions(args.input_file)
    summary = summarize_transactions(transactions)

    with open(args.output_file, 'w') as f:
        for category, total in summary.items():
            f.write(f"{category}: {total:.2f} руб.\n")

    print(f"Отчет успешно сохранен в {args.output_file}.")
