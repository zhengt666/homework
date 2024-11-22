import numpy as np
from scipy.optimize import fsolve
from typing import List
import itertools
import networkx as nx
from domian import ProjectCashFlows
from SALib.sample import saltelli
from SALib.analyze import sobol
import matplotlib.pyplot as plt

# npv 可行性分析
def feasibility_check(cash_flows, discount_rate):
    npv_value = npv(cash_flows, discount_rate)
    print(f"Net Present Value (NPV): {npv_value}")
    irr_value = irr(cash_flows)
    print(f"Internal Rate of Return (IRR): {irr_value * 100:.2f}%")

    # 判断方案是否可行
    if npv_value > 0 and irr_value > discount_rate:
        print("方案可行。")
    else:
        print("方案不可行。")

# 计算净现值
def npv(cash_flows, discount_rate):
    n = len(cash_flows)
    return sum(cash_flows[i] / (1 + discount_rate)**i for i in range(n))


# 计算内部收益率
def irr(cash_flows):
    def f(r):
        return sum(cash_flows[i] / (1 + r)**i for i in range(len(cash_flows)))
    return fsolve(f, 0.1)[0]

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

# 计算优劣方案组合
def calc_rank(project_list: List[ProjectCashFlows], rate):
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
        return sorted_projects
    except nx.NetworkXUnfeasible:
        # 如果图包含环，则拓扑排序不可行
        print("The graph contains a cycle and cannot be topologically sorted.")

combinations_list = []

# 计算组合的总收益
def calculate_return(project_list: List[ProjectCashFlows],total_investment):
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

    # 打印结果
    print(f"盈亏平衡产量: {break_even_quantity} 件")
    print(f"盈亏平衡生产能力利率: {break_even_rate}%")
    print(f"盈亏平衡销售价格: {break_even_selling_price} 元/件")
    print(f"盈亏平衡单位产品变动成本: {break_even_variable_cost} 元/件")
    print(f"经营安全率: {safety_margin*100}%")
    
    if safety_margin > 0.5:
        print ("经营安全")
    else:
        print ("经营不安全")
    
    return {
        "break_even_quantity": break_even_quantity,
        "break_even_rate": break_even_rate,
        "break_even_selling_price": break_even_selling_price,
        "break_even_variable_cost": break_even_variable_cost,
        "safety_margin": safety_margin
    } 


def dynamic_payback_period(cash_flows, discount_rate):
    """
    初始投资即第一年年初现金流
    """
    initial_investment = np.abs(cash_flows[0])
    """
    计算动态回收期。
    
    :param initial_investment: 初始投资额
    :param cash_flows: 现金流列表，按时间序列排列
    :param discount_rate: 折现率
    :return: 动态回收期
    """
    cumulative_npv = 0
    payback_period = 0
    for i, cash_flow in enumerate(cash_flows):
        cumulative_npv += cash_flow / (1 + discount_rate) ** (i + 1)
        if cumulative_npv >= initial_investment:
            payback_period = i + 1
            break
    
    # 如果投资没有回收，则返回None
    if cumulative_npv < initial_investment:
        return None
    
    # 计算剩余部分的回收期
    remaining_investment = initial_investment - cumulative_npv + cash_flow / (1 + discount_rate) ** (i + 1)
    for j in range(i + 1, len(cash_flows)):
        cash_flow = cash_flows[j]
        remaining_investment -= cash_flow / (1 + discount_rate) ** (j + 1)
        if remaining_investment <= 0:
            payback_period += (j - i) + 1 - (-remaining_investment / (cash_flow / (1 + discount_rate) ** (j + 1)))
            break
    
    return payback_period