from typing import List

from domian import ProjectAnalysis
from feasibility_utils import generate_combinations,break_even_analysis_extended,dynamic_payback_period_difference,get_projects,get_base_data_openpyxl,feasibility_check,calc_rank,calc_best_combination,calculate_break_even,dynamic_payback_period,draw_cash_flow,draw_single_factor,draw_multi_factor,static_payback_period
from collections import Counter

file_path = "./projects/方案输入数据.xlsx"
discount_rate,total_investment = get_base_data_openpyxl(file_path)

print(f"当前折现率:{discount_rate*100}%,总投资额:{total_investment}")

project_list,project_opposites,project_opposites_name = get_projects(file_path,discount_rate)

feasibility_project_list:List[str] = []

best_project:List[ProjectAnalysis] = []

print("分析项目可行性")
for i in range(len(project_list)):
    if feasibility_check(project_list[i],discount_rate):
        feasibility_project_list.append(project_list[i].project_name)

print("计算所有方案的回收期，以及画出现金流量图")
for project in project_list:
    payback_period_dynamic = dynamic_payback_period(project,discount_rate)
    project.project_dynamic_cycle = payback_period_dynamic
    
    payback_period_static = static_payback_period(project)
    project.project_static_cycle = payback_period_static
    draw_cash_flow(project)


for i in range(len(project_opposites)):
    print(f"方案{project_opposites_name[i]}大小店方案")
    project_big = project_opposites[i][0]
    project_small = project_opposites[i][1]
    print("方案\t期初投资\t净现值\t寿命\t动态回收期")
    print(f"{project_big.project_name}\t{project_big.project_invest}\t{project_big.project_npv}\t{project_big.project_period}\t{project_big.project_dynamic_cycle}")
    print(f"{project_small.project_name}\t{project_small.project_invest}\t{project_small.project_npv}\t{project_small.project_period}\t{project_small.project_dynamic_cycle}")
    if project_big.project_name not in feasibility_project_list or project_small.project_name not in feasibility_project_list:
        print(f"方案{project_opposites_name[i]}含有不可行方案，不进行对比")
        continue
    print(f"方案{project_opposites_name[i]}方案比选")
    best_npv_project = ''
    if project_big.project_npv > project_small.project_npv:
        best_npv_project = project_big.project_name
    else:
        best_npv_project = project_small.project_name
    print(f"根据净现值,方案{best_npv_project}更优")
    rank_list = calc_rank(project_opposites[i],discount_rate)
    print(f"根据差额IRR,方案{project_opposites_name[i]}排列大小店优先级,得出方案{rank_list[0].project_name}更优")
    payback_period_diff = dynamic_payback_period_difference(project_big.project_cash_flows,project_small.project_cash_flows,discount_rate)
    big_payback_period,big_period_project,small_period_project = project_big.project_dynamic_cycle,project_big.project_name,project_small.project_name if  project_big.project_dynamic_cycle > project_small.project_dynamic_cycle else project_small.project_dynamic_cycle,project_small.project_name,project_big.project_name
    best_period_project = ''
    print("根据差额投资回收期对比")
    if payback_period_diff > big_payback_period:
        print(f"差额投资回收期={payback_period_diff} > {big_payback_period}")
        print(f"方案{small_period_project}更优") 
        best_period_project = small_period_project
    else:
        print(f"差额投资回收期={payback_period_diff} <= {big_payback_period}")
        print(f"方案{big_period_project}更优") 
        best_period_project = big_period_project
    arr = [best_npv_project,best_period_project,rank_list[0].project_name]
    counter = Counter(arr)
    print(f"综上所述,方案{max(counter, key=counter.get)}更优")
    ## 将优质方案放置best数组
    best_project.append(project_big) if project_big.project_name == max(counter, key=counter.get) else best_project.append(project_small)
    
    print("盈亏平衡计算")
    print(f"方案{project_big.project_name}的盈亏平衡")
    calculate_break_even(project_big)
    break_even_analysis_extended(project_big.project_fixed_cost,project_big.variable_cost,project_big.project_selling_price,100000)
    
    print(f"方案{project_small.project_name}的盈亏平衡")
    calculate_break_even(project_small)
    break_even_analysis_extended(project_small.project_fixed_cost,project_small.variable_cost,project_small.project_selling_price,100000)
    
    print("敏感性分析")
    print(f"方案{project_big.project_name}的单因素分析")
    draw_single_factor(project_big,discount_rate)
    print(f"方案{project_big.project_name}的多因素分析")
    draw_multi_factor(project_big,discount_rate)
    
    print(f"方案{project_small.project_name}的单因素分析")
    draw_single_factor(project_small,discount_rate)
    print(f"方案{project_small.project_name}的多因素分析")
    draw_multi_factor(project_small,discount_rate)
    
print("总方案分析")
print("互斥方案选择")
for i in range(len(project_opposites_name)):
    print(f"方案{project_opposites_name[i]}大小店互斥，项目选择:{best_project[i].project_name}")

print("独立方案选择")
all_combinations = generate_combinations(best_project)

