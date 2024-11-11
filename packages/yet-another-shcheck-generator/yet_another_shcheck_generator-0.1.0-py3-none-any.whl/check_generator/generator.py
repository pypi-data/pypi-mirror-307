import argparse
import json

def generate_check(input_file, output_file):
    try:
        with open(input_file, 'r') as f:
            order_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        return

    customer_name = order_data['customer_name']
    items = order_data['items']

    total_sum = 0
    with open(output_file, 'w') as outfile:
        outfile.write(f"Чек для: {customer_name}\n\n")
        for item in items:
            item_total = item['quantity'] * item['price']
            outfile.write(f"{item['name']} x {item['quantity']}: {item_total} руб.\n")
            total_sum += item_total

        outfile.write(f"\nИтого: {total_sum} руб.\n")


def main():
    parser = argparse.ArgumentParser(description="Генерация чека.")
    parser.add_argument("--input-file", required=True, help="Входной JSON-файл")
    parser.add_argument("--output-file", required=True, help="Выходной TXT-файл")
    args = parser.parse_args()
    generate_check(args.input_file, args.output_file)



if __name__ == "__main__":
    main()