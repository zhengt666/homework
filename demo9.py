import numpy as np
import matplotlib.pyplot as plt



# 定义净现值计算函数
def calculate_npv_multi(K, B, C, r, n, X, Y, Z):
    return -K * (1 + X) + (B * (1 + Y) - C * (1 + Z)) * (1 - (1 + r) ** -n) / r

def draw_multi_factor(K,B,C,r,n):
    # 设置变动范围
    X_range = np.linspace(-0.2, 0.2, 100)  # 投资额变动范围 -20% 到 20%
    Y_range = np.linspace(-0.2, 0.2, 100)  # 年销售收入变动范围 -20% 到 20%
    Z_range = np.array([0.2, 0.1, 0, -0.1, -0.2])  # 经营成本变动范围 +20% 到 -20%

    # 创建网格
    X, Y = np.meshgrid(X_range, Y_range)

    # 计算NPV
    NPV = np.zeros_like(X)
    for i, z in enumerate(Z_range):
        NPV += calculate_npv_multi(K, B, C, r, n, X, Y, z) / len(Z_range)

    # 绘制等高线图
    plt.figure(figsize=(10, 6))
    contour = plt.contour(X, Y, NPV, levels=[0], colors='black')
    plt.clabel(contour, inline=True, fontsize=8)
    plt.xlabel('Investment Change (%)')
    plt.ylabel('Sales Revenue Change (%)')
    plt.title('Multi-Factor Sensitivity Analysis')
    plt.grid(True)
    plt.show()


# 定义基础数据
K = 1000  # 初始投资额（万元）
B = 700   # 年销售收入（万元）
C = 400   # 年经营成本（万元）
r = 0.10  # 折现率
n = 10    # 项目期限（年）

draw_multi_factor(K,B,C,r,n)