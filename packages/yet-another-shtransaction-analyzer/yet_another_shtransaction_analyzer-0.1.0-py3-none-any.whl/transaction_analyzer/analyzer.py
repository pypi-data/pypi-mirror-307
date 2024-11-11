import argparse
import pandas as pd

def analyze_transactions(input_file, output_file):
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        return

    income = df[df['type'] == 'income']['amount'].sum()
    expenses = df[df['type'] == 'expense']['amount'].sum()
    
    with open(output_file, 'w') as f:
      f.write(f"Доход: {income:.2f} руб.\n")
      f.write(f"Расход: {expenses:.2f} руб.\n")

def main():
    parser = argparse.ArgumentParser(description='Анализ транзакций.')
    parser.add_argument('--input-file', required=True, help='Входной CSV-файл')
    parser.add_argument('--output-file', required=True, help='Выходной TXT-файл')
    args = parser.parse_args()
    
    analyze_transactions(args.input_file, args.output_file)

if __name__ == '__main__':
    main()