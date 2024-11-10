import pandas as pd
import argparse


# Определение возрастных групп
def age_group(age: int):
    if 18 <= age <= 25:
        return "18-25"
    elif 26 <= age <= 35:
        return "26-35"
    elif 36 <= age <= 45:
        return "36-45"
    elif 46 <= age <= 60:
        return "46-60"
    else:
        return "60+"


def write_to_file(output_file: str, content: str):
    try:
        with open(output_file, 'w') as f:
            f.write(content)
    except (IOError, OSError) as e:
        print(f"Ошибка при записи в файл: {e}")


def analyze_customers(input_file: str, output_file: str):
    df = pd.read_csv(input_file)
    total_customers = len(df)
    df['age_group'] = df['age'].apply(age_group)
    age_distribution = df['age_group'].value_counts()
    city_distribution = df['city'].value_counts()

    lines = [f"Общее количество клиентов: {total_customers}",
             "",
             "Распределение клиентов по возрастным группам:"]
    for group, count in age_distribution.items():  
        lines.append(f"{group}: {count}")
    lines.append("")
    
    lines.append("Распределение клиентов по городам:")
    for city, count in city_distribution.items():
        lines.append(f"{city}: {count}")

    content = "\n".join(lines)
    write_to_file(output_file, content)


def main():
    # Определение аргументов командной строки
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-file', type=str, required=True)
    parser.add_argument('--output-file', type=str, required=True)

    args = parser.parse_args()

    # Запуск анализа
    analyze_customers(args.input_file, args.output_file)


# Чтобы можно было запускать напрямую через командную строку
if __name__ == '__main__':
    main()
