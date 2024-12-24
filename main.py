from typing import List
import logging
from domian import ProjectAnalysis
from feasibility_utils import generate_combinations,break_even_analysis_extended,dynamic_payback_period_difference,get_projects,get_base_data_openpyxl,feasibility_check,calc_rank,calc_best_combination,calculate_break_even,dynamic_payback_period,draw_cash_flow,draw_single_factor,draw_multi_factor,static_payback_period
from collections import Counter

# 配置logging模块，设置日志级别、格式以及输出的文件名
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='./out/output.log',
                    filemode='w')

file_path = "./projects/uploaded_file.xlsx"
discount_rate,total_investment = get_base_data_openpyxl(file_path)

logging.info(f"当前折现率:{discount_rate*100}%,总投资额:{total_investment}")

project_list,project_opposites,project_opposites_name = get_projects(file_path,discount_rate)

feasibility_project_list:List[str] = []

best_project:List[ProjectAnalysis] = []

logging.info("分析项目可行性")
for i in range(len(project_list)):
    if feasibility_check(project_list[i],discount_rate):
        feasibility_project_list.append(project_list[i].project_name)

logging.info("计算所有方案的回收期，以及画出现金流量图")
for project in project_list:
    payback_period_dynamic = dynamic_payback_period(project,discount_rate)
    project.project_dynamic_cycle = payback_period_dynamic
    
    payback_period_static = static_payback_period(project)
    project.project_static_cycle = payback_period_static
    draw_cash_flow(project)


for i in range(len(project_opposites)):
    logging.info(f"方案{project_opposites_name[i]}大小店方案")
    project_big = project_opposites[i][0]
    project_small = project_opposites[i][1]
    logging.info("方案\t期初投资\t净现值\t寿命\t动态回收期")
    logging.info(f"{project_big.project_name}\t{project_big.project_invest}\t{project_big.project_npv}\t{project_big.project_period}\t{project_big.project_dynamic_cycle}")
    logging.info(f"{project_small.project_name}\t{project_small.project_invest}\t{project_small.project_npv}\t{project_small.project_period}\t{project_small.project_dynamic_cycle}")
    if project_big.project_name not in feasibility_project_list or project_small.project_name not in feasibility_project_list:
        logging.info(f"方案{project_opposites_name[i]}含有不可行方案，不进行对比")
        continue
    logging.info(f"方案{project_opposites_name[i]}方案比选")
    best_npv_project = ''
    if project_big.project_npv > project_small.project_npv:
        best_npv_project = project_big.project_name
    else:
        best_npv_project = project_small.project_name
    logging.info(f"根据净现值,方案{best_npv_project}更优")
    rank_list = calc_rank(project_opposites[i],discount_rate)
    logging.info(f"根据差额IRR,方案{project_opposites_name[i]}排列大小店优先级,得出方案{rank_list[0].project_name}更优")

    logging.info("根据差额投资回收期对比")
    payback_period_diff = dynamic_payback_period_difference(project_big.project_cash_flows,project_small.project_cash_flows,discount_rate)
    big_payback_period =project_big.project_dynamic_cycle if  project_big.project_dynamic_cycle > project_small.project_dynamic_cycle else project_small.project_dynamic_cycle

    best_period_project = ''
    if payback_period_diff > big_payback_period:
        logging.info(f"差额投资回收期={payback_period_diff} > {big_payback_period}")
        logging.info(f"方案{project_small.project_name}更优") 
        best_period_project = project_small.project_name
    else:
        logging.info(f"差额投资回收期={payback_period_diff} <= {big_payback_period}")
        logging.info(f"方案{project_big.project_name}更优") 
        best_period_project = project_big.project_name
    print(f"根据差额投资回收期对比,方案{best_period_project}更优")
    arr = [best_npv_project,best_period_project,rank_list[0].project_name]
    counter = Counter(arr)
    logging.info(f"综上所述,方案{max(counter, key=counter.get)}更优")
    ## 将优质方案放置best数组
    best_project.append(project_big) if project_big.project_name == max(counter, key=counter.get) else best_project.append(project_small)
    
    logging.info("盈亏平衡计算")
    logging.info(f"方案{project_big.project_name}的盈亏平衡")
    calculate_break_even(project_big)
    break_even_analysis_extended(project_big.project_fixed_cost,project_big.variable_cost,project_big.project_selling_price,100000)
    
    logging.info(f"方案{project_small.project_name}的盈亏平衡")
    calculate_break_even(project_small)
    break_even_analysis_extended(project_small.project_fixed_cost,project_small.variable_cost,project_small.project_selling_price,100000)
    
    logging.info("敏感性分析")
    logging.info(f"方案{project_big.project_name}的单因素分析")
    draw_single_factor(project_big,discount_rate)
    logging.info(f"方案{project_big.project_name}的多因素分析")
    draw_multi_factor(project_big,discount_rate)
    
    logging.info(f"方案{project_small.project_name}的单因素分析")
    draw_single_factor(project_small,discount_rate)
    logging.info(f"方案{project_small.project_name}的多因素分析")
    draw_multi_factor(project_small,discount_rate)
    
logging.info("总方案分析")
logging.info("互斥方案选择")
for i in range(len(project_opposites_name)):
    logging.info(f"方案{project_opposites_name[i]}大小店互斥，项目选择:{best_project[i].project_name}")

logging.info("独立方案选择")
logging.info(f"方案名\t方案编号\t投资\tIRR\tNPV")
for i in range(len(project_opposites_name)):
    logging.info(f"{project_opposites_name[i]}\t{best_project[i].project_name}\t{best_project[i].project_invest}\t{best_project[i].project_irr}\t{best_project[i].project_npv}")
all_combinations = generate_combinations(best_project)
logging.info(f"方案组合分析\t{len(all_combinations)}种组合方案")
logging.info("组合序号\t组合方式\t总投资\t总NPV")
best_npv = 0
best_index = 0
best_invest = 0
best_combination = ""
best_irr = ""
for i in range(len(all_combinations)):
    project_combination = ""
    total_investment_project = 0
    total_npv_project = 0
    project_irr = ""
    if len(all_combinations[i]) != 0:
        for j in range(len(all_combinations[i])):
            project_combination += f"{all_combinations[i][j].project_name},"
            project_irr += f"{all_combinations[i][j].project_irr*100}%,"
            total_investment_project+= all_combinations[i][j].project_invest * 10000
            total_npv_project += all_combinations[i][j].project_npv * 10000
    else:
        project_combination = ","
        project_irr = ","
    project_combination = project_combination[:-1]
    logging.info(f"{i+1}\t{project_combination}\t{total_investment_project}\t{total_npv_project}")
    if total_investment_project <= total_investment and total_npv_project > best_npv:
        best_index = i
        best_invest = total_investment_project
        best_combination = project_combination
        best_irr = project_irr[:-1]
        best_npv = total_npv_project
logging.info(f"假设总投资{total_investment}以内")
logging.info(f"选择{best_combination}方案，总净现值{round(best_npv,2)},IRR分别为{best_irr},总投资为{round(best_invest,2)}")
