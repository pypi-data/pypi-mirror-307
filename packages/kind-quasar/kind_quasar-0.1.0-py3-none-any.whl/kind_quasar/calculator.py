def calculate_net_profit(revenue, costs):
    return revenue - costs


def calculate_roi(net_profit, costs):
    if costs == 0:
        return 0.0
    return (net_profit / costs) * 100
