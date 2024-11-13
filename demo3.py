import numpy as np
from itertools import combinations

# 假设的方案数据，包括投资额和预期收益
projects = [
    {'investment': 100, 'return': 120},
    {'investment': 220, 'return': 250},
    {'investment': 150, 'return': 180},
    {'investment': 300, 'return': 360},
    {'investment': 250, 'return': 300}
]

# 固定的总投资额
total_investment = 500

# 计算组合的总收益
def calculate_return(combination):
    total_return = 0
    total_invest = 0
    for project in combination:
        total_return += project['return']
        total_invest += project['investment']
    return total_return if total_invest <= total_investment else 0

# 生成所有可能的组合
combinations_list = []
for r in range(1, len(projects) + 1):
    combinations_list.extend(list(combinations(projects, r)))

# 找到最优组合
best_combination = max(combinations_list, key=calculate_return)

print(f"Best combination: {best_combination}")
print(f"Total return of best combination: {calculate_return(best_combination)}")