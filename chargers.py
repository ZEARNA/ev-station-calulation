def calculate_project(power, price, qty, utilization, charge_price, electricity_cost):

    energy_day = power * qty * utilization * 24

    revenue_day = energy_day * charge_price

    electricity_day = energy_day * electricity_cost

    annual_profit = (revenue_day - electricity_day) * 365

    project_cost = price * qty

    roi = None

    if annual_profit > 0:
        roi = project_cost / annual_profit

    return project_cost, annual_profit, roi
