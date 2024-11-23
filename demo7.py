import matplotlib.pyplot as plt
import numpy as np

# 颜色设置
arrow_color = 'black'
axis_color = 'black'
title_color = 'black'

# 设置绘图标题
plt.title("现金流量图", c=title_color)
plt.ylabel("资金（万元）")

# 设置初始变量值
distance = 50
A = [[-600, 0, 0, 0, 0, 0, 0],
     [0, 350, 350, 450, 450, 450, 450],
     [0, -200, -200, -250, -250, -250, -250]]

# 根据列表绘制资金流量图
for j in range(len(A)):
    for i in range(len(A[j])):
        if A[j][i] > 0:
            plt.arrow(i, 0, 0, A[j][i] - distance, fc=arrow_color, ec=arrow_color, shape="full", head_width=0.1, head_length=distance, overhang=0.5)
            plt.text(i + len(A) * 0.01, A[j][i] + distance, str(round(A[j][i], 2)))
        elif A[j][i] < 0:
            plt.arrow(i, 0, 0, A[j][i] + distance, fc=arrow_color, ec=arrow_color, shape="full", head_width=0.1, head_length=distance, overhang=0.5)
            plt.text(i + len(A) * 0.01, A[j][i] - distance, str(round(A[j][i], 2)))

# 设置图表中各个元素的特征
ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['bottom'].set_position(('data', 0))
plt.setp(ax.xaxis.get_majorticklabels(), ha="left")
plt.arrow(-0.1, 0, len(A[0]) + 1.2, 0, fc=axis_color, ec=axis_color, shape="full", head_width=distance * 0.5, head_length=0.3, overhang=0.5)
plt.yticks([])
x_major_locator = plt.MultipleLocator(1)
ax.xaxis.set_major_locator(x_major_locator)
plt.xlim(-0.1, len(A[0]) + 1.4)
plt.ylim(-15 * distance, 15 * distance)

# 调整中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 绘图
plt.show()
