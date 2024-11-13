import numpy as np
from SALib.sample import saltelli
from SALib.analyze import sobol
import matplotlib.pyplot as plt

# 定义问题
problem = {
    'num_vars': 1,
    'names': ['factor'],
    'bounds': [[0.8, 1.2]]
}

# 生成样本
param_values = saltelli.sample(problem, 1000)

# 假设基础现金流数据
base_cash_flows = [100, 120, 150, 180, 200]

# 计算不同参数值下的净现值
npvs = []
for params in param_values:
    adjusted_cash_flows = [cf * params[0] for cf in base_cash_flows]
    npv = sum(cf / (1 + 0.1)**i for i, cf in enumerate(adjusted_cash_flows))
    npvs.append(npv)

# 进行 Sobol 分析
Si = sobol.analyze(problem, np.array(npvs))  # 将 npvs 转换为 numpy 数组

# 提取敏感性指标
s1 = Si['S1'][0]

# 画出敏感性折线图
x = np.linspace(0.8, 1.2, len(npvs))
plt.plot(x, npvs)
plt.xlabel('Factor')
plt.ylabel('Net Present Value')
plt.title('Sensitivity Analysis')
plt.show()