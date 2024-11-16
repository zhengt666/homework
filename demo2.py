import numpy as np
from scipy.optimize import fsolve
from typing import List
import itertools
import networkx as nx

# 定义项目的现金流数据和周期
project1_cash_flows = [-1000, 300, 400, 500, 600]
project2_cash_flows = [-800, 250, 350, 450, 550, 200]
project3_cash_flows = [-1200, 350, 450, 550, 650, 300, 200]

class ProjectCashFlows:
    project_name = ""
    project_cash_flows = []
    project_period = 0

    def __init__(self, project_name, project_cach_flows):
        self.project_name = project_name
        self.project_cash_flows = project_cach_flows
        self.project_period = len(project_cach_flows)

project1 = ProjectCashFlows("1",project1_cash_flows)
project2 = ProjectCashFlows("2",project2_cash_flows)
project3 = ProjectCashFlows("3",project3_cash_flows)

project_list = [project1,project2,project3]

# 计算单个项目的内部收益率，处理不同周期
def irr(cash_flows):
    def f(r):
        return sum(cash_flows[i] / (1 + r)**i for i in range(len(cash_flows)))
    return fsolve(f, 0.1)[0]

# 计算项目之间的差额内部收益率，扩展到不同周期
def diff_irr(cash_flows1, cash_flows2):
    max_period = max(len(cash_flows1), len(cash_flows2))
    extended_cash_flows1 = cash_flows1 + [0] * (max_period - len(cash_flows1))
    extended_cash_flows2 = cash_flows2 + [0] * (max_period - len(cash_flows2))
    combined_cash_flows = [a - b for a, b in zip(extended_cash_flows1, extended_cash_flows2)]
    return irr(combined_cash_flows)

def diff_calc(project_list: List[ProjectCashFlows], rate):
    for project in project_list:
        calc_irr = irr(project.project_cash_flows)
        print(f"Project {project.project_name} IRR: {calc_irr * 100:.2f}%")

    # 两两组合对比
    combinations = list(itertools.combinations(project_list, 2))
 
    diff_irrs = []
    # 打印结果
    for combo in combinations:
        print(f"compare {combo[0].project_name} and {combo[1].project_name}")
        calc_diff_irr = diff_irr(combo[0].project_cash_flows, combo[1].project_cash_flows)
        print(f"Difference IRR between Project {combo[0].project_name} and Project {combo[1].project_name}: {calc_diff_irr * 100:.2f}%")
        if calc_diff_irr < rate:
            diff_irrs.append((combo[1],combo[0]))
        else:
            diff_irrs.append((combo[0],combo[1]))
    
    print(diff_irrs)
    # 创建有向图
    G = nx.DiGraph()
    # 添加边（对比关系）
    edges = diff_irrs
    G.add_edges_from(edges)
    
    try:
        # 尝试进行拓扑排序
        # 注意：在networkx的某些版本中，这个函数可能叫做lexicographical_topological_sort
        sorted_projects = list(nx.topological_sort(G))
        # 如果你的networkx版本没有topological_sort，尝试使用以下代码：
        # sorted_projects = list(nx.lexicographical_topological_sort(G))
        
        # 输出排序结果
        print(f"Project priorities: {sorted_projects}")
        return sorted_project
    except nx.NetworkXUnfeasible:
        # 如果图包含环，则拓扑排序不可行
        print("The graph contains a cycle and cannot be topologically sorted.")
    
diff_calc(project_list,0.2)