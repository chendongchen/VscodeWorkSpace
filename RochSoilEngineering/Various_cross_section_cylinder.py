import numpy as np
from scipy.integrate import solve_bvp
import matplotlib.pyplot as plt

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 定义参数
E = 1000
r = lambda x: (x**2)/200 + 25/2
A = lambda x: np.pi * r(x)**2

# 定义微分方程的一阶形式
def ode(x, U):
    # U = [u, u']
    dUdx = [
        U[1],
        - (np.gradient(A(x), x) / A(x)) * U[1]  # 展开导数项后的表达式
    ]
    return np.vstack(dUdx)

# 定义边界条件
def bc(Ua, Ub):
    # Ua 是 x=0 处的状态 [u(0), u'(0)]
    # Ub 是 x=50 处的状态 [u(50), u'(50)]
    return [
        Ua[0] - 0,          # u(0) = 0
        Ub[1] + 1/E         # u'(50) = -1/E
    ]

# 生成初始网格和猜测值
x_span = np.linspace(0, 50, 100)
U_guess = np.zeros((2, x_span.size))

# 数值求解
sol = solve_bvp(ode, bc, x_span, U_guess)

# 提取结果
x_points = np.linspace(0, 50, 100)
u_numerical = sol.sol(x_points)[0]

# 绘图
plt.plot(x_points, u_numerical, 'b-', label='数值解')
plt.xlabel('x')
plt.ylabel('u(x)')
plt.legend()
plt.title('变系数二阶方程数值解')
plt.show()
