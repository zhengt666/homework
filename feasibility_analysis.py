from domian import ProjectAnalysis
from typing import List
from feasibility_utils import is_float,upload_excel_files,feasibility_check,calc_rank,calc_best_combination,calculate_break_even,dynamic_payback_period,draw_cash_flow,draw_single_factor,draw_multi_factor,static_payback_period
import tkinter as tk
from tkinter import simpledialog,messagebox


# 确认用户是否要批量上传
user_confirmation = messagebox.askyesno("批量上传确认", "请批量上传Excel文件")
if not user_confirmation:
    exit()
# 调用函数以上传Excel文件
upload_excel_files()

# 创建一个主窗口（虽然在这个例子中不会显示它）
root = tk.Tk()
root.withdraw()  # 隐藏主窗口

# 使用 simpledialog 弹出一个输入框
discount_rate_str = simpledialog.askstring("折现率", "请输入一个小数,1为100%:")
if discount_rate_str is None or not is_float(discount_rate_str):
    exit()
# 折现率
discount_rate = float(discount_rate_str)

total_investment_str = simpledialog.askstring("总投资额", "请输入总投资额:")
if total_investment_str is None or not is_float(total_investment_str):
    exit()
total_investment = float(total_investment_str)
print(f"当前折现率:{discount_rate*100}%,总投资额:{total_investment}")

#projectA = ProjectAnalysis("德庄火锅",[0,816,816,816,816,816],[182.4,661.35,669.09,676.91,687.95,696.99],335,700,200*340,0.012,discount_rate,["潮发牛肉火锅店","海鲜自助火锅"])
#projectB = ProjectAnalysis("潮发牛肉火锅店",[0,1020,1020,1020,1020,1020+10+5],[147,847.65,847.65,847.65,847.65,847.65],500,900,300*340,0.007,discount_rate,["德庄火锅","海鲜自助火锅"])
projectC = ProjectAnalysis("海鲜自助火锅",[0,567,567,567,567,567,610.98],[97,443.9,443.9,443.9,443.9,443.9,443.9],300,600,200*340,0.007,discount_rate,["潮发牛肉火锅店","德庄火锅"])


#project_list = [projectA,projectB,projectC]
project_list = [projectC]

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



