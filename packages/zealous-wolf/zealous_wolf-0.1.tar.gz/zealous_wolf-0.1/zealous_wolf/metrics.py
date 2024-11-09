import argparse


def calculate_net_profit(revenue, costs):
    return revenue - costs


def calculate_roi(net_profit, costs):
    if costs == 0:
        return 0.0
    return (net_profit / costs) * 100


def main():
    parser = argparse.ArgumentParser(description='Calculate net profit and ROI.')
    parser.add_argument('--revenue', type=float, required=True, help='Total revenue')
    parser.add_argument('--costs', type=float, required=True, help='Total costs')

    args = parser.parse_args()

    net_profit = calculate_net_profit(args.revenue, args.costs)
    roi = calculate_roi(net_profit, args.costs)

    print(f'Чистая прибыль: {net_profit:.2f} руб.')
    print(f'ROI: {roi:.2f}%')


if __name__ == '__main__':
    main()
