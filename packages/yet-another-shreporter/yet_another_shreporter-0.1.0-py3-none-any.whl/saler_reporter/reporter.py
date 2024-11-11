import argparse
import pandas as pd

def generate_sales_report(input_file, output_file):
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        return
    report = df.groupby('category').agg({'sales': 'sum', 'quantity': 'sum'})
    report.to_csv(output_file)


def main():
    parser = argparse.ArgumentParser(description='Генерация отчёта по продажам.')
    parser.add_argument('--input-file', required=True, help='Входной CSV-файл')
    parser.add_argument('--output-file', required=True, help='Выходной CSV-файл')
    args = parser.parse_args()

    generate_sales_report(args.input_file, args.output_file)

if __name__ == '__main__':
    main()