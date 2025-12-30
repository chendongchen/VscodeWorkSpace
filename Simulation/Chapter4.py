import numpy as np

# 设置全局打印选项，保留5位有效数字
np.set_printoptions(precision=5, suppress=True)

# 定义一个矩阵 A（设置为 float 类型）
A = np.array([
    [5.0, 2.0, 1.0],
    [-1.0, 4.0, 2.0],
    [2.0, -3.0, 10.0]
], dtype=float)

x = np.array([0.0, 0.0, 0.0], dtype=float)

b = np.array([-12.0, 20.0, 3.0], dtype=float)

def direct_solution(A, b):
    try:
        x = np.linalg.solve(A, b)
        print("直接解法的解:", x)
        return x
    except np.linalg.LinAlgError as e:
        print("无法求解方程组:", e)
        return None

def jacobi_iteration(A, b, x, max_iterations=100, tolerance=1e-2):
    n = len(A)
    
    for iteration in range(max_iterations):
        y = x.copy()
        for i in range(n):
            sum_of_terms = 0
            for j in range(n):
                if j != i:
                    sum_of_terms += A[i, j] * y[j]
            x[i] = (b[i] - sum_of_terms) / A[i, i]
        error = np.max(np.abs(x - y))
        if error < tolerance:
            print(f"第 {iteration + 1} 次迭代的解: {x}  误差: {error:.5f}")
            print("jacobi迭代的解成功收敛")
            return x
        print(f"第 {iteration + 1} 次迭代的解: {x}  误差: {error:.5f}")

    return x

def gauss_seidel_iteration(A, b, x, max_iterations=100, tolerance=1e-2):
    n = len(A)
    
    for iteration in range(max_iterations):
        y = x.copy()
        for i in range(n):
            sum_of_terms = 0
            for j in range(n):
                if j != i:
                    sum_of_terms += A[i, j] * x[j]
            x[i] = (b[i] - sum_of_terms) / A[i, i]
        error = np.max(np.abs(x - y))
        if error < tolerance:
            print(f"第 {iteration + 1} 次迭代的解: {x}  误差: {error:.5f}")
            print("gauss_seidel迭代的解成功收敛")
            return x
        print(f"第 {iteration + 1} 次迭代的解: {x}  误差: {error:.5f}")
    return x

def sor_iteration(A, b, x, omega=0.9, max_iterations=100, tolerance=1e-2):
    n = len(A)
    
    for iteration in range(max_iterations):
        y = x.copy()
        for i in range(n):
            sum_of_terms = 0
            for j in range(n):
                if j != i:
                    sum_of_terms += A[i, j] * x[j]
            x[i] = (1 - omega) * y[i] + (omega * (b[i] - sum_of_terms) / A[i, i])
        error = np.max(np.abs(x - y))
        if error < tolerance:
            print(f"第 {iteration + 1} 次迭代的解: {x}  误差: {error:.5f}")
            print("sor迭代的解成功收敛")
            return x
        print(f"第 {iteration + 1} 次迭代的解: {x}  误差: {error:.5f}")

    return x

def main():
    print("直接解法:")
    x_direct = direct_solution(A, b)
    print("最终解:", x_direct)
    print("Jacobi迭代:")
    x_jacobi = jacobi_iteration(A, b, x.copy())
    print("最终解:", x_jacobi)
    
    print()
    print("Gauss-Seidel迭代:")       
    x_gauss_seidel = gauss_seidel_iteration(A, b, x.copy())        
    print("最终解:", x_gauss_seidel)    
    
    print()
    print("SOR迭代:")
    x_sor = sor_iteration(A, b, x.copy())
    print("最终解:", x_sor)
    
    print()     

if __name__ == "__main__":
    main()

# 结果：
# 直接解法:
# 直接解法的解: [-4.  3.  2.]
# 最终解: [-4.  3.  2.]
# Jacobi迭代:
# 第 1 次迭代的解: [-2.4  5.   0.3]  误差: 5.00000
# 第 2 次迭代的解: [-4.46  4.25  2.28]  误差: 2.06000
# 第 3 次迭代的解: [-4.556  2.745  2.467]  误差: 1.50500
# 第 4 次迭代的解: [-3.9914  2.6275  2.0347]  误差: 0.56460
# 第 5 次迭代的解: [-3.85794  2.9848   1.88653]  误差: 0.35730
# 第 6 次迭代的解: [-3.97123  3.09225  1.96703]  误差: 0.11329
# 第 7 次迭代的解: [-4.03031  3.02368  2.02192]  误差: 0.06857
# 第 8 次迭代的解: [-4.01386  2.98146  2.01316]  误差: 0.04222
# 第 9 次迭代的解: [-3.99522  2.98995  1.99721]  误差: 0.01864
# 第 10 次迭代的解: [-3.99542  3.00259  1.99603]  误差: 0.01264
# 第 11 次迭代的解: [-4.00024  3.00313  1.99986]  误差: 0.00482
# jacobi迭代的解成功收敛
# 最终解: [-4.00024  3.00313  1.99986]

# Gauss-Seidel迭代:
# 第 1 次迭代的解: [-2.4  4.4  2.1]  误差: 4.40000
# 第 2 次迭代的解: [-4.58    2.805   2.0575]  误差: 2.18000
# 第 3 次迭代的解: [-3.9335   2.98787  1.98306]  误差: 0.64650
# 第 4 次迭代的解: [-3.99176  3.01053  2.00151]  误差: 0.05826
# 第 5 次迭代的解: [-4.00451  2.99812  2.00034]  误差: 0.01275
# 第 6 次迭代的解: [-3.99931  3.       1.99986]  误差: 0.00520
# gauss_seidel迭代的解成功收敛
# 最终解: [-3.99931  3.       1.99986]

# SOR迭代:
# 第 1 次迭代的解: [-2.16     4.014    1.74258]  误差: 4.01400
# 第 2 次迭代的解: [-4.1347   3.18693  2.04898]  误差: 1.97470
# 第 3 次迭代的解: [-4.08958  2.9765   2.01468]  误差: 0.21043
# 第 4 次迭代的解: [-4.00314  2.99034  1.99942]  误差: 0.08644
# 第 5 次迭代的解: [-3.99673  3.00003  1.99936]  误差: 0.00969
# sor迭代的解成功收敛
# 最终解: [-3.99673  3.00003  1.99936]