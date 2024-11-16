import numpy as np
from itertools import combinations
from project_cash_flows import ProjectCashFlows

# 定义项目的现金流数据和周期
project1_cash_flows = [-1000, 300, 400, 500, 600]
project2_cash_flows = [-800, 250, 350, 450, 550, 200]
project3_cash_flows = [-1200, 350, 450, 550, 650, 300, 200]

project1 = ProjectCashFlows("1",project1_cash_flows,1000)
project2 = ProjectCashFlows("2",project2_cash_flows,800)
project3 = ProjectCashFlows("3",project3_cash_flows,1200)

project_list = [project1,project2,project3]

# 固定的总投资额
total_investment = 2500

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