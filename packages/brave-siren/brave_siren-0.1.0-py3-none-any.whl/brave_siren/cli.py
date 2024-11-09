from .generator import load_order_data, generate_receipt, save_receipt
import argparse


def main():
    parser = argparse.ArgumentParser(description="Generate a receipt from order data.")
    parser.add_argument('--input-file', type=str, required=True, help='Input JSON file with order data')
    parser.add_argument('--output-file', type=str, required=True, help='Output text file for the receipt')

    args = parser.parse_args()

    order_data = load_order_data(args.input_file)
    receipt = generate_receipt(order_data)

    save_receipt(receipt, args.output_file)

    print(f"Чек успешно сохранен в {args.output_file}.")
