from .calculator import calculate_net_profit, calculate_roi
import argparse


def main():
    parser = argparse.ArgumentParser(description="Calculate financial metrics.")
    parser.add_argument('--revenue', type=float, required=True, help='Total revenue')
    parser.add_argument('--costs', type=float, required=True, help='Total costs')

    args = parser.parse_args()

    net_profit = calculate_net_profit(args.revenue, args.costs)
    roi = calculate_roi(net_profit, args.costs)

    print(f"Чистая прибыль: {net_profit:.2f} руб.")
    print(f"ROI: {roi:.2f}%")
