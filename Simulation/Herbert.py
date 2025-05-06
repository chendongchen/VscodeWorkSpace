import numpy as np

def hilbert_matrix(n):
    """生成 Hilbert 矩阵 Hn"""
    H = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            H[i, j] = 1 / (i + j + 1)
    return H

def cholesky_decomposition(A):
    """Cholesky 分解"""
    n = A.shape[0]
    L = np.zeros_like(A)
    for i in range(n):
        for j in range(i + 1):
            if i == j:
                L[i, j] = np.sqrt(A[i, i] - np.sum(L[i, :j] ** 2))
            else:
                L[i, j] = (A[i, j] - np.sum(L[i, :j] * L[j, :j])) / L[j, j]
    return L

def solve_cholesky(L, b):
    """用 Cholesky 分解求解方程"""
    # 前向替换求解 Ly = b
    y = np.zeros_like(b)
    for i in range(len(b)):
        y[i] = (b[i] - np.dot(L[i, :i], y[:i])) / L[i, i]
    
    # 后向替换求解 L^T x = y
    x = np.zeros_like(b)
    for i in range(len(b) - 1, -1, -1):
        x[i] = (y[i] - np.dot(L.T[i, i + 1:], x[i + 1:])) / L.T[i, i]
    
    return x

def compute_and_print_results(n):
    """计算并打印结果"""
    # 生成 Hilbert 矩阵 Hn 和向量 b
    H = hilbert_matrix(n)
    x_true = np.ones(n)
    b = np.dot(H, x_true)
    
    # Cholesky 分解求解
    L = cholesky_decomposition(H)
    x_approx = solve_cholesky(L, b)
    
    # 计算残差和误差的 ∞-范数
    r = b - np.dot(H, x_approx)
    delta_x = x_approx - x_true
    r_norm = np.linalg.norm(r, ord=np.inf)
    delta_x_norm = np.linalg.norm(delta_x, ord=np.inf)
    
    # 格式化输出为科学计数法，保留 4 位有效数字
    np.set_printoptions(formatter={'float': '{:.4e}'.format})
    
    print(f"n = {n}")
    #  print("近似解 x̂:", x_approx)
    print("残差 r 的 ∞-范数:", f"{r_norm:.4e}")
    print("误差 Δx 的 ∞-范数:", f"{delta_x_norm:.4e}")
    print()

def main_function_1():
    n = 10  # 设置 Hilbert 矩阵的维度为 10
    compute_and_print_results(n)

def main_function_2(n_perturb):
    n = n_perturb  # 设置 Hilbert 矩阵的维度为 10
    
    # 生成 Hilbert 矩阵 Hn 和向量 b
    H = hilbert_matrix(n)
    x_true = np.ones(n)
    b = np.dot(H, x_true)
    
    # 在 b 上施加 10^-7 的扰动
    b_perturbed = b + 1e-7 * np.random.randn(n)
    
    # Cholesky 分解求解原方程
    L = cholesky_decomposition(H)
    x_approx = solve_cholesky(L, b)
    
    # Cholesky 分解求解扰动后的方程
    x_approx_perturbed = solve_cholesky(L, b_perturbed)
    
    # 计算残差和误差的 ∞-范数
    r = b - np.dot(H, x_approx)
    delta_x = x_approx - x_true
    r_norm = np.linalg.norm(r, ord=np.inf)
    delta_x_norm = np.linalg.norm(delta_x, ord=np.inf)
    
    # 计算扰动后的残差和误差的 ∞-范数
    r_perturbed = b_perturbed - np.dot(H, x_approx_perturbed)
    delta_x_perturbed = x_approx_perturbed - x_true
    r_perturbed_norm = np.linalg.norm(r_perturbed, ord=np.inf)
    delta_x_perturbed_norm = np.linalg.norm(delta_x_perturbed, ord=np.inf)
    
    # 格式化输出为科学计数法，保留 4 位有效数字
    np.set_printoptions(formatter={'float': '{:.4e}'.format})
    
    print()
    print("n = ", n)
    print("原方程残差 r 的 ∞-范数:", f"{r_norm:.4e}")
    print("原方程误差 Δx 的 ∞-范数:", f"{delta_x_norm:.4e}")
    print()
    print("扰动 b = b + 10^-7")
    print("扰动后方程残差 r 的 ∞-范数:", f"{r_perturbed_norm:.4e}")
    print("扰动后方程误差 Δx 的 ∞-范数:", f"{delta_x_perturbed_norm:.4e}")
    print()

def main_function_3():
    # 分别计算 n = 8 和 n = 12 的情况
    for n in [8, 12]:
        main_function_2(n)

def main():
    
    print("第一小问,n = 10")
    main_function_1()
    
    print("第二小问, n = 10, 扰动 b = b + 10^-7")
    main_function_2(10)
    
    print("第三小问, 分别计算 n = 8 和 n = 12 的情况")
    main_function_3()

if __name__ == "__main__":
    main()

# 第一小问,n = 10
# n = 10
# 残差 r 的 ∞-范数: 2.2204e-16
# 误差 Δx 的 ∞-范数: 4.0884e-05

# 第二小问, n = 10, 扰动 b = b + 10^-7

# n =  10
# 原方程残差 r 的 ∞-范数: 2.2204e-16
# 原方程误差 Δx 的 ∞-范数: 4.0884e-05

# 扰动 b = b + 10^-7
# 扰动后方程残差 r 的 ∞-范数: 6.7395e-12
# 扰动后方程误差 Δx 的 ∞-范数: 2.6885e+05

# 第三小问, 分别计算 n = 8 和 n = 12 的情况

# n =  8
# 原方程残差 r 的 ∞-范数: 2.2204e-16
# 原方程误差 Δx 的 ∞-范数: 1.0652e-06

# 扰动 b = b + 10^-7
# 扰动后方程残差 r 的 ∞-范数: 8.8818e-15
# 扰动后方程误差 Δx 的 ∞-范数: 2.8283e+02


# n =  12
# 原方程残差 r 的 ∞-范数: 2.2204e-16
# 原方程误差 Δx 的 ∞-范数: 1.4107e-01

# 扰动 b = b + 10^-7
# 扰动后方程残差 r 的 ∞-范数: 2.6576e-09
# 扰动后方程误差 Δx 的 ∞-范数: 1.1023e+08