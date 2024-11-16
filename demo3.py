import numpy as np
from itertools import combinations
from project_cash_flows import ProjectCashFlows
from typing import List

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

combinations_list = []

# 计算组合的总收益
def calculate_return(project_list: List[ProjectCashFlows]):
    total_return = 0
    total_invest = 0
    for project in project_list:
        combinations_list.append(project)
        total_return += project.project_invest
        total_invest += project.project_npv
    return total_return if total_invest <= total_investment else 0

def calc_best_combination(project_list: List[ProjectCashFlows]):
    print(f"Total return of best combination: {calculate_return(project_list)}")
    print(f"Best combination: {combinations_list}")
    return combinations_list