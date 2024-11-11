import argparse

def calculate_net_profit(revenue, costs):
    return revenue - costs

def calculate_roi(net_profit, costs):
    return (net_profit / costs) * 100 if costs else 0  # Обработка деления на ноль

def main():
    parser = argparse.ArgumentParser(description="Расчёт финансовых показателей.")
    parser.add_argument("--revenue", type=float, required=True, help="Доходы компании")
    parser.add_argument("--costs", type=float, required=True, help="Расходы компании")
    args = parser.parse_args()

    net_profit = calculate_net_profit(args.revenue, args.costs)
    roi = calculate_roi(net_profit, args.costs)

    print(f"Чистая прибыль: {net_profit:.2f} руб.")
    print(f"ROI: {roi:.2f}%")

if __name__ == "__main__":
    main()