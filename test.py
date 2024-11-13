import matplotlib.pyplot as plt  
import numpy as np  
import matplotlib  
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
matplotlib.rcParams['axes.unicode_minus']=False#中文字体状态下负号（-）正常显示

def get_equation(x_vlaue,y_vlaue):
    # 计算斜率和截距  
    m = (y_vlaue[1] - y_vlaue[0]) / (x_vlaue[1] - x_vlaue[0])  
    b = y_vlaue[0] - m * x_vlaue[0]  
    
    # 格式化方程字符串  
    return m,b,f"y = {m:.1f}x + {b:.1f}"  # 使用.1f来限制小数点后一位  
  
# 定义第一组数据点（线1）  
x1_values = [-1, 3]  
y1_values = [-2, -4]  
  
# 定义第二组数据点（线2）  
x2_values = [1, 3]  
y2_values = [1, 5]  # 注意这里y值不同，以形成不同的线  
# 创建一个新的图形  
fig, ax = plt.subplots()  
  
# 设置轴的比例相等，这样象限看起来才是正方形的  
ax.set_aspect('equal')  
  
# 绘制x轴和y轴  
ax.axhline(0, color='black',linewidth=0.5)  # y=0的水平线  
ax.axvline(0, color='black',linewidth=0.5)  # x=0的垂直线  
  
# 设置轴的范围  
ax.set_xlim(-5, 5)  
ax.set_ylim(-5, 5)    
# 如果有更多线，可以继续定义x3_values, y3_values等  
m,b,equation = get_equation(x1_values,y1_values);
x_line = np.linspace(min(x1_values) - 1, max(x1_values) + 1, 400)
y_line = m * x_line + b  
# 绘制第一条线  
plt.plot(x_line, y_line,linestyle='-', color='b', label=f'{equation}')  

m,b,equation = get_equation(x2_values,y2_values);
x_line = np.linspace(min(x2_values) - 1, max(x2_values) + 1, 400)
y_line = m * x_line + b  
# 绘制第二条线  
plt.plot(x_line, y_line, linestyle='-', color='r', label=f'{equation}')  
  
# 如果有更多线，可以继续调用plt.plot()  
  
# 添加标题和标签  
plt.title('多条线的线型图')  
plt.xlabel('X 轴')  
plt.ylabel('Y 轴')  
  
# 显示图例  
plt.legend()  
  
# 显示网格  
plt.grid(True)  
  
# 显示图表  
plt.show()


