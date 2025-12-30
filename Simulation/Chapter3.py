import numpy as np
from scipy.linalg import lu

def partial_pivoting_lu_decomposition(A):
    """
    实现部分主元LU分解算法，返回置换矩阵P、下三角矩阵L和上三角矩阵U。
    """
    n = A.shape[0]
    P = np.eye(n)  # 初始化置换矩阵为单位矩阵
    L = np.zeros((n, n), dtype=float)  # 初始化下三角矩阵为浮点类型
    U = A.astype(float)  # 将上三角矩阵初始化为A的浮点副本

    for i in range(n):
        # 寻找当前列的主元（绝对值最大元素的行索引）
        max_row = np.argmax(np.abs(U[i:, i])) + i

        # 如果需要，进行行交换
        if max_row != i:
            U[[i, max_row], :] = U[[max_row, i], :]
            P[[i, max_row], :] = P[[max_row, i], :]
            if i > 0:
                L[[i, max_row], :i] = L[[max_row, i], :i]

        # 计算L和U
        for j in range(i + 1, n):
            L[j, i] = U[j, i] / U[i, i]
            U[j, i:] -= L[j, i] * U[i, i:]

    np.fill_diagonal(L, 1)  # 将L的对角线元素设置为1
    return P, L, U


# 定义一个矩阵 A
A = np.array([
    [1, 2, 3],
    [2, 4, 5],
    [3, 5, 6]
])

# 进行LU分解（部分主元高斯消去）
P, L, U = partial_pivoting_lu_decomposition(A)

# 输出结果
print("矩阵 A:")
print(A)

print("\n置换矩阵 P:")
print(P)

print("\n下三角矩阵 L:")
print(L)

print("\n上三角矩阵 U:")
print(U)

# 定义另一个矩阵 B
B = np.array([
    [2, 1, 1, 2],
    [2, 2, 2, 2],
    [4, 2, 4, 3],
    [0, 0, 6, -1]
])

# 进行LU分解（部分主元高斯消去）
P, L, U = partial_pivoting_lu_decomposition(B)

# 输出结果
print("\n矩阵 B:")
print(B)

print("\n置换矩阵 P:")
print(P)

print("\n下三角矩阵 L:")
print(L)

print("\n上三角矩阵 U:")
print(U)

# 5
# 进行LU分解（高斯消去）
# 定义另一个矩阵 B
# 定义一个矩阵 A
A = np.array([
    [1, 1, 1],
    [2, 2, 1],
    [3, 3, 1]
])

# 进行LU分解（部分主元高斯消去）
L, U = lu(A)

# 输出结果
print("\n矩阵 A:")
print(A)

print("\n置换矩阵 P:")
print(P)

print("\n下三角矩阵 L:")
print(L)

print("\n上三角矩阵 U:")
print(U)

A = np.array([
    [1, 2, 3],
    [2, 4, 1],
    [4, 6, 7]
])

# 进行LU分解（部分主元高斯消去）
L, U = lu(A)

# 输出结果
print("\n矩阵 A:")
print(A)

print("\n置换矩阵 P:")
print(P)

print("\n下三角矩阵 L:")
print(L)

print("\n上三角矩阵 U:")
print(U)