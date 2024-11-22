def calculate_break_even(fixed_cost, total_cost, production_capacity, selling_price):
    # 计算变动成本
    variable_cost = (total_cost - fixed_cost) / production_capacity
    
    # 计算盈亏平衡产量
    break_even_quantity = fixed_cost / (selling_price - variable_cost)
    
    # 计算盈亏平衡生产能力利率
    break_even_rate = (break_even_quantity / production_capacity) * 100
    
    # 计算盈亏平衡销售价格
    break_even_selling_price = variable_cost + (fixed_cost / production_capacity)
    
    # 计算盈亏平衡单位产品变动成本
    break_even_variable_cost = selling_price - (fixed_cost / production_capacity)
    
    # 计算经营安全率
    safety_margin = 1 - (break_even_quantity / production_capacity)

    if safety_margin > 0.5:
        print ("经营安全")
    
    return {
        "break_even_quantity": break_even_quantity,
        "break_even_rate": break_even_rate,
        "break_even_selling_price": break_even_selling_price,
        "break_even_variable_cost": break_even_variable_cost,
        "safety_margin": safety_margin
    }

# 示例数据
fixed_cost = 30000  # 固定成本
total_cost = 230000  # 总成本
production_capacity = 20000  # 年设计生产能力
selling_price = 15  # 产品售价

# 计算盈亏平衡点
break_even_points = calculate_break_even(fixed_cost, total_cost, production_capacity, selling_price)

# 打印结果
print(f"盈亏平衡产量: {break_even_points['break_even_quantity']} 件")
print(f"盈亏平衡生产能力利率: {break_even_points['break_even_rate']}%")
print(f"盈亏平衡销售价格: {break_even_points['break_even_selling_price']} 元/件")
print(f"盈亏平衡单位产品变动成本: {break_even_points['break_even_variable_cost']} 元/件")
print(f"经营安全率: {break_even_points['safety_margin']*100}%")
