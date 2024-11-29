import numpy as np
from scipy.optimize import fsolve

# 假设的现金流数据，你可以根据实际情况进行修改
cash_flows = [-279.65, 137.53, 137.53, 137.53, 137.53,137.53+97.25+15]

# 设定贴现率，你可以根据实际情况调整
discount_rate = 0.1

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


feasibility_check(cash_flows,discount_rate)