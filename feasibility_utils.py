import numpy as np
from scipy.optimize import fsolve
from typing import List
import itertools
import networkx as nx
from domian import ProjectAnalysis
import matplotlib.pyplot as plt



# npv 可行性分析
def feasibility_check(project:ProjectAnalysis, discount_rate):
    print(f"project {project.project_name} 可行性分析")
    npv_value = npv(project.project_cash_flows, discount_rate)
    print(f"Net Present Value (NPV): {npv_value}")
    irr_value = irr(project.project_cash_flows)
    print(f"Internal Rate of Return (IRR): {irr_value * 100:.2f}%")

    # 判断方案是否可行
    if npv_value > 0 and irr_value > discount_rate:
        print(f"project {project.project_name} 方案可行。")
        return True
    else:
        print(f"project {project.project_name} 方案不可行。")
        return False

# 计算净现值
def npv(cash_flows, discount_rate):
    n = len(cash_flows)
    for j in range(n):
        a = round(cash_flows[j] / (1 + discount_rate)**j,2)
        print(f"npv 第{j}年 {a}")
    return round(sum(round(cash_flows[i] / (1 + discount_rate)**i,2) for i in range(n)),2)


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
def calc_rank(project_list: List[ProjectAnalysis], rate) -> List[ProjectAnalysis]:
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
        
        return sorted_projects
    except nx.NetworkXUnfeasible:
        # 如果图包含环，则拓扑排序不可行
        print("The graph contains a cycle and cannot be topologically sorted.")

combinations_list:List[ProjectAnalysis] = []

# 计算组合的总收益
def calculate_return(project_list: List[ProjectAnalysis],total_investment):
    total_return = 0
    total_invest = 0
    for project in project_list:
        total_invest += project.project_invest
        if total_invest >= total_investment:
            total_invest -= project.project_invest
            continue
        combinations_list.append(project)
        total_return += project.project_npv
    return total_return

# 最优方案选择
def calc_best_combination(project_list: List[ProjectAnalysis],total_investment:float) -> List[ProjectAnalysis]:
    print(f"Total return of best combination: {calculate_return(project_list,total_investment)}")
    print(f"Best combination: { ','.join([obj.project_name for obj in combinations_list])}")
    return combinations_list

# 计算盈亏平衡
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

# 计算动态回收期
def dynamic_payback_period(project:ProjectAnalysis, discount_rate):
    
    """
    初始投资即第一年年初现金流
    """
    initial_investment = np.abs(project.project_cash_flows[0])
    """
    计算动态回收期。
    
    :param initial_investment: 初始投资额
    :param cash_flows: 现金流列表，按时间序列排列
    :param discount_rate: 折现率
    :return: 动态回收期
    """
    cumulative_npv = 0
    payback_period = 0
    for i, cash_flow in enumerate(project.project_cash_flows):
        cumulative_npv += cash_flow / (1 + discount_rate) ** (i + 1)
        if cumulative_npv >= initial_investment:
            payback_period = i + 1
            break
    
    # 如果投资没有回收，则返回None
    if cumulative_npv < initial_investment:
        return None
    
    # 计算剩余部分的回收期
    remaining_investment = initial_investment - cumulative_npv + cash_flow / (1 + discount_rate) ** (i + 1)
    for j in range(i + 1, len(project.project_cash_flows)):
        cash_flow = project.project_cash_flows[j]
        remaining_investment -= cash_flow / (1 + discount_rate) ** (j + 1)
        if remaining_investment <= 0:
            payback_period += (j - i) + 1 - (-remaining_investment / (cash_flow / (1 + discount_rate) ** (j + 1)))
            break
    print(f"计算 project:{project.project_name} 的动态回收期为: {payback_period}")
    return payback_period

# 绘制现金流量图
def draw_cash_flow(project:ProjectAnalysis):
    # 颜色设置
    arrow_color = 'black'
    axis_color = 'black'
    title_color = 'black'

    # 调整中文显示
    plt.rcParams['font.sans-serif'] = ['PingFang SC']
    plt.rcParams['axes.unicode_minus'] = False
    # 设置绘图标题
    plt.title(f"Cash Flow Diagram of {project.project_name}", c=title_color)
    plt.ylabel("Funds (in ten thousand yuan)")

    # 设置初始变量值
    distance = 100
    negative_array = [-x for x in project.project_cash_flows_out]
    cash_flow_array : List[List[int]] = [project.project_cash_flows_in,negative_array]

    # 根据列表绘制资金流量图
    for j in range(len(cash_flow_array)):
        for i in range(len(cash_flow_array[j])):
            if cash_flow_array[j][i] > 0:
                plt.arrow(i, 0, 0, cash_flow_array[j][i] - distance, fc=arrow_color, ec=arrow_color, shape="full", head_width=0.1, head_length=distance, overhang=0.5)
                plt.text(i + len(cash_flow_array) * 0.01, cash_flow_array[j][i] + distance, str(round(cash_flow_array[j][i], 2)))
            elif cash_flow_array[j][i] < 0:
                plt.arrow(i, 0, 0, cash_flow_array[j][i] + distance, fc=arrow_color, ec=arrow_color, shape="full", head_width=0.1, head_length=distance, overhang=0.5)
                plt.text(i + len(cash_flow_array) * 0.01, cash_flow_array[j][i] - distance, str(round(cash_flow_array[j][i], 2)))

    # 设置图表中各个元素的特征
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['bottom'].set_position(('data', 0))
    plt.setp(ax.xaxis.get_majorticklabels(), ha="left")
    plt.arrow(-0.1, 0, len(cash_flow_array[0]) + 1.2, 0, fc=axis_color, ec=axis_color, shape="full", head_width=distance * 0.5, head_length=0.3, overhang=0.5)
    plt.yticks([])
    x_major_locator = plt.MultipleLocator(1)
    ax.xaxis.set_major_locator(x_major_locator)
    plt.xlim(-0.1, len(cash_flow_array[0]) + 1.4)
    plt.ylim(-15 * distance, 15 * distance)


    # 绘图
    plt.show()
    

# 定义净现值计算函数
def calculate_npv_single(K, B, C, r, n):
    return -K + (B - C) * (1 - (1 + r) ** -n) / r

# 定义单因素敏感性分析函数
def single_factor_sensitivity_analysis(factor, base_value, r, n, variation_range,K,B,C):
    npv_values = []
    for variation in variation_range:
        new_value = base_value * (1 + variation / 100)
        npv = calculate_npv_single(K, B, C, r, n) if factor == 'K' else calculate_npv_single(K if factor == 'B' else new_value, B if factor == 'C' else new_value, C, r, n)
        npv_values.append(npv)
    return npv_values

# 绘制单因素分析
def draw_single_factor(K,B,C,r,n):
    # 设置变动范围
    variation_range = np.arange(-20, 21, 5)

    # 分析投资额、年销售收入和年经营成本的敏感性
    npv_K = single_factor_sensitivity_analysis('K', K, r, n, variation_range,K,B,C)
    npv_B = single_factor_sensitivity_analysis('B', B, r, n, variation_range,K,B,C)
    npv_C = single_factor_sensitivity_analysis('C', C, r, n, variation_range,K,B,C)

    # 绘制敏感性分析图
    plt.figure(figsize=(10, 6))
    plt.plot(variation_range, npv_K, label='Investment Sensitivity')
    plt.plot(variation_range, npv_B, label='Sales Revenue Sensitivity')
    plt.plot(variation_range, npv_C, label='Operating Cost Sensitivity')
    plt.xlabel('Variation (%)')
    plt.ylabel('NPV (10,000 yuan)')
    plt.title('Single Factor Sensitivity Analysis')
    plt.legend()
    plt.grid(True)
    plt.show()
    


# 定义净现值计算函数
def calculate_npv_multi(K, B, C, r, n, X, Y, Z):
    return -K * (1 + X) + (B * (1 + Y) - C * (1 + Z)) * (1 - (1 + r) ** -n) / r

# 绘制多因素分析
def draw_multi_factor(K,B,C,r,n):
    # 设置变动范围
    X_range = np.linspace(-0.2, 0.2, 100)  # 投资额变动范围 -20% 到 20%
    Y_range = np.linspace(-0.2, 0.2, 100)  # 年销售收入变动范围 -20% 到 20%
    Z_range = np.array([0.2, 0.1, 0, -0.1, -0.2])  # 经营成本变动范围 +20% 到 -20%

    # 创建网格
    X, Y = np.meshgrid(X_range, Y_range)

    # 计算NPV
    NPV = np.zeros_like(X)
    for i, z in enumerate(Z_range):
        NPV += calculate_npv_multi(K, B, C, r, n, X, Y, z) / len(Z_range)

    # 绘制等高线图
    plt.figure(figsize=(10, 6))
    contour = plt.contour(X, Y, NPV, levels=[0], colors='black')
    plt.clabel(contour, inline=True, fontsize=8)
    plt.xlabel('Investment Change (%)')
    plt.ylabel('Sales Revenue Change (%)')
    plt.title('Multi-Factor Sensitivity Analysis')
    plt.grid(True)
    plt.show()