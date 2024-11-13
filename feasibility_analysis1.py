import numpy as np
from SALib.sample import saltelli
from SALib.analyze import sobol
import matplotlib.pyplot as plt

# 定义本量利分析模型函数
def cvp_model(params):
    fixed_cost, variable_cost_per_unit, selling_price_per_unit = params
    quantity = np.arange(1, 1000)
    total_cost = fixed_cost + variable_cost_per_unit * quantity
    total_revenue = selling_price_per_unit * quantity
    return total_cost[-1], total_revenue[-1]

# 定义问题参数
problem_cvp = {
    'num_vars': 3,
    'names': ['fixed_cost', 'variable_cost_per_unit', 'selling_price_per_unit'],
    'bounds': [[1000, 5000], [10, 30], [50, 100]]
}

# 进行采样
sample_cvp = saltelli.sample(problem_cvp, 1024)

# 计算模型结果
costs = []
revenues = []
for params in sample_cvp:
    cost, revenue = cvp_model(params)
    costs.append(cost)
    revenues.append(revenue)

total_costs = np.array(costs)
total_revenues = np.array(revenues)

try:
    # 进行敏感性分析
    Si_cvp = sobol.analyze(problem_cvp, total_costs)
except Exception as e:
    print(f"Error during sensitivity analysis: {e}")

# 绘制本量利分析图
for i in range(len(sample_cvp)):
    plt.plot(np.arange(1, 1000)[-1], costs[i], alpha=0.2, color='blue', marker='o')
    plt.plot(np.arange(1, 1000)[-1], revenues[i], alpha=0.2, color='orange', marker='o')
plt.title('Cost-Volume-Profit Analysis')
plt.xlabel('Quantity')
plt.ylabel('Cost/Revenue')
plt.legend(['Total Cost', 'Total Revenue'])
plt.show()

# 绘制敏感性分析折线图
try:
    plt.figure(figsize=(8, 6))
    plt.plot(problem_cvp['names'], Si_cvp['S1'], marker='o', label='First-order index')
    plt.title('Sensitivity Analysis for CVP')
    plt.xlabel('Variable')
    plt.ylabel('Sensitivity Index')
    plt.legend()
    plt.show()
except Exception as e:
    print(f"Error during plotting sensitivity analysis: {e}")