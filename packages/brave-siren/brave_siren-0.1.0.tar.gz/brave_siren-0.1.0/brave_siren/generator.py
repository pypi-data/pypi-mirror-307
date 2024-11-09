import json


def load_order_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def generate_receipt(order_data):
    customer_name = order_data['customer_name']
    items = order_data['items']

    total_amount = sum(item['quantity'] * item['price'] for item in items)

    receipt_lines = [f"Чек для: {customer_name}\n"]
    receipt_lines.append("Товары:\n")

    for item in items:
        line = f"{item['name']} - {item['quantity']} шт. по {item['price']} руб.\n"
        receipt_lines.append(line)

    receipt_lines.append(f"\nОбщая сумма: {total_amount} руб.\n")

    return ''.join(receipt_lines)


def save_receipt(receipt, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(receipt)
