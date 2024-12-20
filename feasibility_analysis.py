from domian import ProjectAnalysis
from typing import List
from feasibility_utils import get_projects,get_base_data_openpyxl,feasibility_check,calc_rank,calc_best_combination,calculate_break_even,dynamic_payback_period,draw_cash_flow,draw_single_factor,draw_multi_factor,static_payback_period

file_path = "./projects/方案输入数据.xlsx"
discount_rate,total_investment = get_base_data_openpyxl(file_path)

print(f"当前折现率:{discount_rate*100}%,总投资额:{total_investment}")

project_list = get_projects(file_path,discount_rate)

feasibility_project_list:List[ProjectAnalysis] = []

print("分析项目可行性")
for i in range(len(project_list)):
    if feasibility_check(project_list[i],discount_rate):
        feasibility_project_list.append(project_list[i])

print("计算可行方案的动态回收期，以及画出现金流量图")
for project in feasibility_project_list:
    payback_period_dynamic = dynamic_payback_period(project,discount_rate)
    project.project_dynamic_cycle = payback_period_dynamic
    
    payback_period_static = static_payback_period(project)
    project.project_static_cycle = payback_period_static
    draw_cash_flow(project)
    
print("排列项目优先")
rank_list = calc_rank(feasibility_project_list,discount_rate)
print("当前优先排列")
for i in range(len(rank_list)):
    print(f"{rank_list[i].project_name}")


print("组合最优方案")
best_combined = calc_best_combination(rank_list,total_investment)

combined_investment = sum(p.project_invest for p in best_combined)
less_investment = total_investment - combined_investment
print(f"投资金额总数:{combined_investment}")
print(f"剩余投资金额：{less_investment}")

print("最佳组合方案盈亏，敏感性分析")
for project in best_combined:
    print(f"筛选方案{project.project_name}的盈亏平衡")
    calculate_break_even(project)

    print(f"筛选方案{project.project_name}的单因素分析")
    draw_single_factor(project,discount_rate)

    print(f"筛选方案{project.project_name}的多因素分析")
    draw_multi_factor(project,discount_rate)



