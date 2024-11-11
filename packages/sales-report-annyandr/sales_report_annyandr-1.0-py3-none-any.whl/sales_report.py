import argparse
import pandas as pd

def load_sales_data(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")

def save_report(report, output_file):
    try:
        report.to_csv(output_file, index=True)
        print(f"Отчёт сохранён в файл {output_file}")
    except IOError:
        print(f"Ошибка записи в файл: {e}")
    except Exception as e:
        print(f"Ошибка при сохранении отчёта: {e}")

def generate_report(input_file: str, output_file: str):
    sales_data = load_sales_data(input_file)
    report = sales_data.groupby('category').agg({'sales': 'sum', 'quantity': 'sum'})
    save_report(report, output_file)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input-file',
        type=str,
        required=True)
    parser.add_argument(
        '--output-file',
        type=str, 
        required=True)

    args = parser.parse_args()
    generate_report(args.input_file, args.output_file)

if __name__ == '__main__':
    main()
