import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

# 初始化打印设置，确保以分数形式输出
sp.init_printing(use_unicode=False)

# 使用 Rational 定义矩阵元素，确保以分数形式处理
A  = sp.Matrix([[sp.Rational(2, 1), sp.Rational(2, 3), sp.Rational(2, 5)],
                [sp.Rational(2, 3), sp.Rational(2, 5), sp.Rational(2, 7)],
                [sp.Rational(2, 5), sp.Rational(2, 7), sp.Rational(2, 9)]])
b = sp.Matrix([sp.Rational(1, 1), sp.Rational(1, 2), sp.Rational(1, 3)])

# 求解方程 A * x = b
x = A.solve(b)

# 转化为数值形式
x_numeric = [float(val) for val in x]

# 输出符号解
print("符号解为:")
sp.pprint(x)

# 验证解是否正确
is_correct = A * x == b
print("\n验证解是否正确:", is_correct)

# 构造多项式，仅包含 0 次、2 次和 4 次项
# 假设解的第一个值为 0 次项系数，第二个值为 2 次项系数，第三个值为 4 次项系数
coefficients = [x_numeric[0], 0, x_numeric[1], 0, x_numeric[2]]
poly = np.poly1d(coefficients[::-1])  # 将系数从高次到低次排列

# 定义绘图范围
x_vals = np.linspace(-1, 1, 500)
y_vals = poly(x_vals)

# 计算 |x| 的值
abs_y_vals = np.abs(x_vals)

# 绘制多项式曲线
plt.plot(x_vals, y_vals, label="Polynomial Curve (0, 2, 4 terms)", color="blue")
# 绘制 |x| 曲线
plt.plot(x_vals, abs_y_vals, label="|x| Curve", color="red", linestyle="--")

# 添加图像标题和标签
plt.title("Polynomial Plot with 0, 2, 4 Terms and |x| Comparison")
plt.xlabel("x")
plt.ylabel("y")
plt.axhline(0, color='black', linewidth=0.5, linestyle='--')
plt.axvline(0, color='black', linewidth=0.5, linestyle='--')

# 设置横纵坐标长度相同
plt.axis('equal')

plt.legend()
plt.grid()
plt.show()

# 符号解为:
# [ 15  ]
# [ --- ]
# [ 128 ]
# [     ]
# [ 105 ]
# [ --- ]
# [ 64  ]
# [     ]
# [-105 ]
# [-----]
# [ 128 ]