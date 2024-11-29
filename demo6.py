import numpy as np

def dynamic_payback_period(cash_flows, discount_rate):
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
        cash_year = cash_flow / (1 + discount_rate) ** (i)
        cumulative_npv += cash_year
        if cumulative_npv >= 0:
            remaining_year = round(1 - (cumulative_npv / cash_year),2)
            payback_period = i - 1 + remaining_year
            break
    
    # 如果投资没有回收，则返回None
    if cumulative_npv < 0:
        return None
    return payback_period

cash_flows = [-164.95, 120.96, 120.96, 120.96, 120.96,120.96+67.95+10]
discount_rate = 0.1  # 折现率5%

# 计算动态回收期
payback_period = dynamic_payback_period(cash_flows, discount_rate)
print(f"动态回收期: {payback_period}")