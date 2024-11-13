import numpy as np  
from SALib.sample import saltelli  
from SALib.analyze import sobol  
from SALib.test_functions import Ishigami  
  
# 定义问题：输入参数的数量、名称和边界  
problem = {  
    'num_vars': 3,  
    'names': ['x1', 'x2', 'x3'],  
    'bounds': [[-3.14159265359, 3.14159265359], [-3.14159265359, 3.14159265359], [-3.14159265359, 3.14159265359]]  
}  
  
# 生成样本  
param_values = saltelli.sample(problem, 1024)  
  
# 运行模型并保存输出（这里使用Ishigami函数作为示例模型）  
Y = Ishigami.evaluate(param_values)  
  
# 计算灵敏度指数  
Si = sobol.analyze(problem, Y, print_to_console=True)  
  
# 提取并处理分析结果  
S1 = Si['S1']  # 一阶指数  
ST = Si['ST']  # 总阶指数  
  
# 可视化分析结果（以线型图为例）  
import matplotlib.pyplot as plt  
import matplotlib  
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
matplotlib.rcParams['axes.unicode_minus']=False#中文字体状态下负号（-）正常显示
plt.figure(figsize=(10, 6))  
plt.plot(problem['names'], S1, marker='o', label='一阶指数 (S1)')  
plt.plot(problem['names'], ST, marker='s', label='总阶指数 (ST)', linestyle='--')  
plt.title('敏感性分析结果')  
plt.xlabel('输入参数')  
plt.ylabel('灵敏度指数')  
plt.legend()  
plt.grid(True)  
plt.show()