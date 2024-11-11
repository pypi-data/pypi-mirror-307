import pandas as pd
import argparse


def load_transactions_data(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")

def save_to_file(output_file: str, content: str):
    try:
        with open(output_file, 'w') as f:
            f.writelines(content)
            print(f"Успешно сохранено в файл {output_file}")
    except IOError:
        print(f"Ошибка записи в файл: {e}")
    except Exception as e:
        print(f"Ошибка при сохранении: {e}")

def count_category(in_file, out_file):
    df = load_transactions_data(in_file)
    grouped_transactions = df.groupby('category')['amount'].sum()
    grouped_transactions = grouped_transactions.to_dict()
    lines = []
    for category_name, value in grouped_transactions.items():
        lines.append(f'{category_name}: {value} руб.\n')
    save_to_file(out_file, lines)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--input-file',
        action='store',
        required=True,
    )

    parser.add_argument(
        '--output-file',
        action='store',
        required=True,
    )

    args = parser.parse_args()
    count_category(args.input_file, args.output_file)


if __name__ == '__main__':
    main()
