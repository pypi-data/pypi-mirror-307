from .analyzer import load_customer_data, analyze_customers, generate_report, save_report
import argparse


def main():
    parser = argparse.ArgumentParser(description="Analyze customer data from a CSV file.")
    parser.add_argument('--input-file', type=str, required=True, help='Input CSV file with customer data')
    parser.add_argument('--output-file', type=str, required=True, help='Output text file for the report')

    args = parser.parse_args()

    customer_data = load_customer_data(args.input_file)
    total_customers, age_distribution, city_distribution = analyze_customers(customer_data)

    report = generate_report(total_customers, age_distribution, city_distribution)
    save_report(report, args.output_file)

    print(f"Отчет успешно сохранен в {args.output_file}.")
