import numpy as np
import matplotlib.pyplot as plt

# 定义净现值计算函数
def calculate_npv(K, B, C, r, n):
    return -K + (B - C) * (1 - (1 + r) ** -n) / r

# 修改后的多因素敏感性分析函数（仅考虑K和B的变化，C固定）
def draw_multi_factor(K, B, C, r, n, Z_fixed):
    # 设置变动范围
    X_range = np.linspace(-0.2, 0.2, 100)  # 投资额变动范围 -20% 到 20%
    Y_range = np.linspace(-0.2, 0.2, 100)  # 年销售收入变动范围 -20% 到 20%

    # 创建网格
    X, Y = np.meshgrid(X_range, Y_range)

    # 计算NPV（C固定为Z_fixed的百分比变化）
    C_fixed = C * (1 + Z_fixed)
    NPV = np.zeros_like(X)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            K_varied = K * (1 + X[i, j])
            B_varied = B * (1 + Y[i, j])
            NPV[i, j] = calculate_npv(K_varied, B_varied, C_fixed, r, n)

    # 绘制等高线图
    plt.figure(figsize=(10, 6))
    contour = plt.contour(X * 100, Y * 100, NPV, levels=[0], colors='black')  # 将X和Y转换为百分比
    plt.clabel(contour, inline=True, fontsize=8)
    plt.xlabel('Investment Change (%)')
    plt.ylabel('Sales Revenue Change (%)')
    plt.title('Multi-Factor Sensitivity Analysis (Fixed Operating Cost Change)')
    plt.grid(True)    
    contour = plt.contour(X, Y, NPV, levels=[0], colors='black')
    plt.clabel(contour, inline=True, fontsize=8)
    plt.show()

# 定义基础数据
K = 1000  # 初始投资额（万元）
B = 700   # 年销售收入（万元）
C = 400   # 年经营成本（万元）
r = 0.10  # 折现率
n = 10    # 项目期限（年）

# 调用函数，固定经营成本变化为0%
draw_multi_factor(K, B, C, r, n, Z_fixed=0.0)