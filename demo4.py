fixed_cost = float(input("请输入固定成本："))
price_per_unit = float(input("请输入单位产品售价："))
variable_cost_per_unit = float(input("请输入单位产品变动成本："))

break_even_point = fixed_cost / (price_per_unit - variable_cost_per_unit)

print(f"盈亏平衡点销售量为：{break_even_point}")