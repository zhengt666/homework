import numpy as np

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

# 示例数据
initial_investment = 1000  # 初始投资额
cash_flows = [200, 300, 400, 500]  # 现金流
discount_rate = 0.05  # 折现率5%

# 计算动态回收期
payback_period = dynamic_payback_period(cash_flows, discount_rate)
print(f"动态回收期: {payback_period}")
