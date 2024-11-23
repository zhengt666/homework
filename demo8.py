import numpy as np
import matplotlib.pyplot as plt



# 定义净现值计算函数
def calculate_npv(K, B, C, r, n):
    return -K + (B - C) * (1 - (1 + r) ** -n) / r

# 定义单因素敏感性分析函数
def single_factor_sensitivity_analysis(factor, base_value, r, n, variation_range):
    npv_values = []
    for variation in variation_range:
        new_value = base_value * (1 + variation / 100)
        npv = calculate_npv(K, B, C, r, n) if factor == 'K' else calculate_npv(K if factor == 'B' else new_value, B if factor == 'C' else new_value, C, r, n)
        npv_values.append(npv)
    return npv_values

def draw_single_factor(K,B,C,i,n):
    # 设置变动范围
    variation_range = np.arange(-20, 21, 5)

    # 分析投资额、年销售收入和年经营成本的敏感性
    npv_K = single_factor_sensitivity_analysis('K', K, i, n, variation_range)
    npv_B = single_factor_sensitivity_analysis('B', B, i, n, variation_range)
    npv_C = single_factor_sensitivity_analysis('C', C, i, n, variation_range)

    # 绘制敏感性分析图
    plt.figure(figsize=(10, 6))
    plt.plot(variation_range, npv_K, label='Investment Sensitivity')
    plt.plot(variation_range, npv_B, label='Sales Revenue Sensitivity')
    plt.plot(variation_range, npv_C, label='Operating Cost Sensitivity')
    plt.xlabel('Variation (%)')
    plt.ylabel('NPV (10,000 yuan)')
    plt.title('Single Factor Sensitivity Analysis')
    plt.legend()
    plt.grid(True)
    plt.show()

# 定义基础数据
K = 1000  # 初始投资额（万元）
B = 700   # 年销售收入（万元）
C = 400   # 年经营成本（万元）
r = 0.10  # 折现率
n = 10    # 项目期限（年）

draw_single_factor(K,B,C,r,n)