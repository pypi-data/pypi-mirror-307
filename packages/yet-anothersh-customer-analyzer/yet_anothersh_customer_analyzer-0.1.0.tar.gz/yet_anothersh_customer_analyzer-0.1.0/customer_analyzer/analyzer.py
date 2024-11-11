import argparse
import pandas as pd

def analyze_customers(input_file, output_file):
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        return

    total_clients = len(df)

    age_groups = {
        '18-25': df[(df['age'] >= 18) & (df['age'] <= 25)].shape[0],
        '26-35': df[(df['age'] >= 26) & (df['age'] <= 35)].shape[0],
        '36-45': df[(df['age'] >= 36) & (df['age'] <= 45)].shape[0],
        '46-60': df[(df['age'] >= 46) & (df['age'] <= 60)].shape[0]
    }

    city_distribution = df['city'].value_counts().to_dict()


    with open(output_file, 'w') as f:
        f.write(f"Общее количество клиентов: {total_clients}\n\n")
        
        f.write("Количество клиентов по возрастным группам:\n")
        for group, count in age_groups.items():
            f.write(f"{group}: {count}\n")


        f.write("\nРаспределение клиентов по городам:\n")
        for city, count in city_distribution.items():
            f.write(f"{city}: {count}\n")



def main():
    parser = argparse.ArgumentParser(description='Анализ клиентской базы.')
    parser.add_argument('--input-file', required=True, help='Входной CSV-файл')
    parser.add_argument('--output-file', required=True, help='Выходной TXT-файл')
    args = parser.parse_args()
    analyze_customers(args.input_file, args.output_file)

if __name__ == '__main__':
    main()