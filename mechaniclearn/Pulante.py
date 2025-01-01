import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

# 定义符号变量
x = sp.symbols('x')

# 定义多个函数
f1 = 1 / (sp.exp(1/x)-1)

# 将符号表达式转换为数值函数
f1_func = sp.lambdify(x, f1, 'numpy')


# 生成 x 值
x_values = np.linspace(0, 10, 4000)

# 计算 y 值
y1_values = f1_func(x_values)


# 绘制函数图像
plt.plot(x_values, y1_values, label='f1(x) ')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.title('Multiple Function Plots')
plt.legend()
plt.grid(True)
plt.show()