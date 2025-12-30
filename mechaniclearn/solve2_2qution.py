import sympy as sp

# 定义符号变量
x, y, z = sp.symbols('x y z')

# 定义多项式函数
polynomial_J = -9 + 18*x + 18*y + 12*z - 12*x*z - 12*y*z - 4*z**2

N =[z*(x + y - 1), z*x, z*y, (1-z)*(x+y-1), (1-z)*x, (1-z)*y]



# 定义积分的上下限
x_limits = (x, 0, 1-y)
y_limits = (y, 0, 1)
z_limits = (z, 0, 1)

# 计算三重积分
num = 0
for polynomial in N:
    num += 1
    poly_n = polynomial_J * polynomial
    # 输出表达式
    print("poly:", poly_n)
    triple_integral = sp.integrate(poly_n, x_limits, y_limits, z_limits)
    # 输出结果
    print("Triple integral:",num, triple_integral)

