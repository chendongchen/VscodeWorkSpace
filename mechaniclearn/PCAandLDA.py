import numpy as np

# 样本集
X = np.array([[-1, 1], [0, 0], [1, -1]])

# 计算样本的均值
mean_X = np.mean(X, axis=0)

# 去中心化样本
X_centered = X - mean_X

# 计算协方差矩阵
cov_matrix = np.cov(X_centered, rowvar=False)

# 特征值分解
eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)

# 按特征值从大到小排序
sorted_indices = np.argsort(eigenvalues)[::-1]
sorted_eigenvalues = eigenvalues[sorted_indices]
sorted_eigenvectors = eigenvectors[:, sorted_indices]

# 第一、第二主成分方向
first_principal_component = sorted_eigenvectors[:, 0]
second_principal_component = sorted_eigenvectors[:, 1]

print("First Principal Component Direction:", first_principal_component)
print("Second Principal Component Direction:", second_principal_component)

# First Principal Component Direction: [ 0.70710678 -0.70710678]
# Second Principal Component Direction: [0.70710678 0.70710678]

# 将样本投影到第一主成分方向上
projection = np.dot(X_centered, first_principal_component)

# 新坐标
new_coordinates = projection.reshape(-1, 1)

print("New Coordinates after Projection on the First Principal Component:")
print(new_coordinates)

# [[-1.41421356]
#  [ 0.        ]
#  [ 1.41421356]]