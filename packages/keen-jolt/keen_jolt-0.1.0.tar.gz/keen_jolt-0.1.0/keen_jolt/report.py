import argparse
import pandas as pd


def load_data(input_file):
    return pd.read_csv(input_file)


def generate_report(data):
    income = data[data['type'] == 'income']['amount'].sum()
    expense = data[data['type'] == 'expense']['amount'].sum()
    report = f"Доход: {income} руб.\nРасход: {expense} руб."
    return report


def main():
    parser = argparse.ArgumentParser(description='Генерация финансового отчета.')
    parser.add_argument('--input-file', required=True, help='Путь к входному CSV-файлу')
    parser.add_argument('--output-file', required=True, help='Путь к выходному TXT-файлу')
    args = parser.parse_args()

    data = load_data(args.input_file)
    report = generate_report(data)
    with open(args.output_file, 'w') as f:
        f.write(report)


if __name__ == "__main__":
    main()
