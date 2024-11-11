import argparse
import json


def load_order_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            order_data = json.load(file)
            return order_data
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")

def save_to_file(output_file: str, content: str):
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(content)
            print(f"Успешно сохранено в файл {output_file}")
    except IOError:
        print(f"Ошибка записи в файл: {e}")
    except Exception as e:
        print(f"Ошибка при сохранении отчёта: {e}")

def generate_receipt(input_file: str, output_file: str):
    order_data = load_order_data(input_file)

    customer_name = order_data['customer_name']
    items = order_data['items']
    total_price = 0
    receipt_lines = [f"Клиент: {customer_name}\n", "Товары:"]
    for item in items:
        item_total = item['quantity'] * item['price']
        receipt_lines.append(f"- {item['name']}, {item['quantity']} шт., {item['price']} руб. за единицу")
        total_price += item_total
    receipt_lines.append(f"\nИтого: {total_price} руб.")

    content = [f"{line}\n" for line in receipt_lines]
    save_to_file(output_file, content)


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

    generate_receipt(args.input_file, args.output_file)

if __name__ == '__main__':
    main()
