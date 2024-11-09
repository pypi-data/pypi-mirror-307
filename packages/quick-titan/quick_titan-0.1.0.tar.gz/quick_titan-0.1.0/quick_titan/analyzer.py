import pandas as pd


def load_customer_data(file_path):
    return pd.read_csv(file_path)


def analyze_customers(customer_data):
    total_customers = len(customer_data)

    age_bins = [18, 25, 35, 45, 60, 100]
    age_labels = ['18-25', '26-35', '36-45', '46-60', '60+']
    customer_data['Age Group'] = pd.cut(customer_data['age'], bins=age_bins, labels=age_labels, right=False)

    age_distribution = customer_data['Age Group'].value_counts().sort_index()

    city_distribution = customer_data['city'].value_counts()

    return total_customers, age_distribution, city_distribution


def generate_report(total_customers, age_distribution, city_distribution):
    report_lines = []
    report_lines.append(f"Общее количество клиентов: {total_customers}\n")

    report_lines.append("Количество клиентов по возрастным группам:\n")
    for age_group, count in age_distribution.items():
        report_lines.append(f"{age_group}: {count}\n")

    report_lines.append("\nРаспределение клиентов по городам:\n")
    for city, count in city_distribution.items():
        report_lines.append(f"{city}: {count}\n")

    return ''.join(report_lines)


def save_report(report, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(report)
