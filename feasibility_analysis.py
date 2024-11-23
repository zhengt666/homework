from domian import ProjectAnalysis
from typing import List
from feasibility_utils import feasibility_check,calc_rank,calc_best_combination,calculate_break_even,dynamic_payback_period,draw_cash_flow,draw_single_factor,draw_multi_factor

# 折现率
discount_rate = 0.1
total_investment = 300
print(f"当前折现率:{discount_rate*100}%,总投资额:{total_investment}")

projectA = ProjectAnalysis("德庄火锅",[0,816,816,816,816,816],[182.4,661.35,669.09,676.91,687.95,696.99],335,700,200*340,0.012,discount_rate)
projectB = ProjectAnalysis("潮发牛肉火锅店",[0,1020,1020,1020,1020,1020+10+5],[147,847.65,847.65,847.65,847.65,847.65],500,900,300*340,0.007,discount_rate)
projectC = ProjectAnalysis("海鲜自助火锅",[0,567,567,567,567,567,610.98],[97,443.9,443.9,443.9,443.9,443.9,443.9],300,600,200*340,0.007,discount_rate)


project_list = [projectA,projectB,projectC]

feasibility_project_list:List[ProjectAnalysis] = []

print("分析项目可行性")
for i in range(len(project_list)):
    if feasibility_check(project_list[i],discount_rate):
        feasibility_project_list.append(project_list[i])

print("计算可行方案的动态回收期，以及画出现金流量图")
for project in feasibility_project_list:
    payback_period = dynamic_payback_period(project,discount_rate)
    project.project_dynamic_cycle = payback_period
    draw_cash_flow(project)
    
print("排列项目优先")
rank_list = calc_rank(feasibility_project_list,discount_rate)
print("当前优先排列")
for i in range(len(rank_list)):
    print(f"{rank_list[i].project_name}")


print("组合最优方案")
best_combined = calc_best_combination(rank_list,total_investment)

print("最佳组合方案盈亏，敏感性分析")
for project in best_combined:
    print("筛选方案的盈亏平衡")
    calculate_break_even(project.project_fixed_cost,project.project_total_cost,project.project_production_capacticy,project.project_selling_price)

    print("筛选方案的单因素分析")
    draw_single_factor(project.project_invest,project.project_cash_flows_in[1],project.project_cash_flows_out[1],discount_rate,project.project_period)

    print("筛选方案的多因素分析")
    draw_multi_factor(project.project_invest,project.project_cash_flows_in[1],project.project_cash_flows_out[1],discount_rate,project.project_period)



