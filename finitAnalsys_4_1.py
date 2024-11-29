# 陈东 2024-11-30日，于国科大雁栖湖校区编写
# 有限元分析作业 作业4第1题 学号202418000531019 班级序号：24
# 运行结果保存到 位移与应力云图./cloud_plots.png 整体刚度矩阵保存到 ./global_stiffness_matrix.xlsx

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.tri import Triangulation
from matplotlib.collections import PolyCollection


# 用户定义节点和单元
nodes = [
    (0, 1),
    (1, 1),
    (0, 0),
    (1, 0),
    (2, 0)
]

elements = [
    [0, 2, 3],  # 第一个单元 注意请按逆时针排列节点坐标，节点从0开始
    [1, 3, 4],  # 第二个单元
    [0, 3, 1]   # 第三个单元
]

E = 210e9  # 弹性模量，单位 Pa
nu = 0.2  # 泊松比
t = 0.01  # 厚度，单位 m
q = 1e6  # 载荷kN/m
f = t * q 
# 提取自由节点 0 和 1 有关的部分
dof_indices = [0, 1, 2, 3]  # 节点 0 和 1 的自由度索引(2n-2,2n-1)

# 定义外力向量
F = np.array([f, 0, 0, 0])  # 假设节点 0 和 1 的外力分别为(F_x,F_y)


# # 示例
# nodes = [
#     (0, 1),
#     (1, 1),
#     (0, 0),
#     (1, 0),
#     (2, 0)
# ]

# elements = [
#     [0, 2, 3],  # 第一个单元
#     [1, 3, 4],  # 第二个单元
#     [0, 3, 1]   # 第三个单元
# ]

# E = 1  # 弹性模量，单位 Pa
# nu = 0.2  # 泊松比
# t = 1  # 厚度，单位 m

# # 提取与节点 0 和 1 有关的部分
# dof_indices = [0, 1, 2, 3]  # 节点 0 和 1 的自由度索引

# # 定义外力向量
# F = np.array([1, 2, 3, 4])  # 假设节点 0 和 1 的外力分别为 (1, 2) 和 (3, 4)


def calculate_area(x1, y1, x2, y2, x3, y3):
    return 0.5 * abs(x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1 - y2))

def calculate_stiffness_matrix(x1, y1, x2, y2, x3, y3, E, nu, t):
    # 计算面积
    A = calculate_area(x1, y1, x2, y2, x3, y3)
    
    # 计算雅可比行列式
    J = 2 * A
    
    # 计算形状函数导数矩阵 B
    B = (1 / (2 * A)) * np.array([
        [y2 - y3, 0, y3 - y1, 0, y1 - y2, 0],
        [0, x3 - x2, 0, x1 - x3, 0, x2 - x1],
        [x3 - x2, y2 - y3, x1 - x3, y3 - y1, x2 - x1, y1 - y2]
    ])
    
    # 计算弹性矩阵 D
    D = (E / (1 - nu**2)) * np.array([
        [1, nu, 0],
        [nu, 1, 0],
        [0, 0, (1 - nu) / 2]
    ])
    
    # 计算刚度矩阵 K
    K = t * B.T @ D @ B * A
    
    return  K, B, D  # 返回 K, B, D

def assemble_global_stiffness_matrix(elements, nodes, E, nu, t):
    num_nodes = len(nodes)
    num_dofs_per_node = 2  # 每个节点有两个自由度
    global_K = np.zeros((num_nodes * num_dofs_per_node, num_nodes * num_dofs_per_node))
    
    for element in elements:
        node_indices = element
        x1, y1 = nodes[node_indices[0]]
        x2, y2 = nodes[node_indices[1]]
        x3, y3 = nodes[node_indices[2]]
        
        local_K, local_B, Local_D = calculate_stiffness_matrix(x1, y1, x2, y2, x3, y3, E, nu, t)
        
        # 映射局部自由度到全局自由度
        dof_map = []
        for node_index in node_indices:
            dof_map.extend([node_index * num_dofs_per_node, node_index * num_dofs_per_node + 1])
        
        for i, global_i in enumerate(dof_map):
            for j, global_j in enumerate(dof_map):
                global_K[global_i, global_j] += local_K[i, j]
    
    return global_K


global_K = assemble_global_stiffness_matrix(elements, nodes, E, nu, t)
# print(global_K)    # 打印刚度矩阵


# 将刚度矩阵保存为 Excel 文件
df = pd.DataFrame(global_K)
df.to_excel('global_stiffness_matrix.xlsx', index=False, header=False)

print("刚度矩阵已保存到 global_stiffness_matrix.xlsx")


reduced_K = global_K[np.ix_(dof_indices, dof_indices)]

print("\n与节点 0 和 1 有关的刚度矩阵:")
print(reduced_K)


# 求解线性方程组
u = np.linalg.solve(reduced_K, F)

print("\n节点 0 和 1 的位移:")
print(u)

# 构建整体节点位移向量
num_nodes = len(nodes)
num_dofs_per_node = 2
u_global = np.zeros(num_nodes * num_dofs_per_node, dtype=np.float64)
u_global[dof_indices] = u

# 计算整体单元节点受力向量
F_total = global_K @ u_global

print("\n整体单元节点受力向量:")
print(F_total)

# 计算每个单元的应力
stress_values = []
for element in elements:
    node_indices = element
    x1, y1 = nodes[node_indices[0]]
    x2, y2 = nodes[node_indices[1]]
    x3, y3 = nodes[node_indices[2]]
    
    # 提取局部节点位移
    dof_indices = []
    for node_index in node_indices:
        dof_indices.append(node_index * num_dofs_per_node)
        dof_indices.append(node_index * num_dofs_per_node + 1)

    local_u = u_global[dof_indices].flatten()
    
    # 计算应力
    K, B, D = calculate_stiffness_matrix(x1, y1, x2, y2, x3, y3, E, nu, t)
    stress = D @ B @ local_u
    stress_values.append(stress)

# 计算每个节点的平均应力
node_stress_sum = np.zeros((num_nodes, 3))  # 每个节点有 σx, σy, τxy 三个应力分量
node_stress_count = np.zeros(num_nodes)  # 记录每个节点关联的单元数量

for i, element in enumerate(elements):
    for node_index in element:
        node_stress_sum[node_index] += stress_values[i]
        node_stress_count[node_index] += 1

node_stress_avg = node_stress_sum / node_stress_count[:, None]

# 绘制云图
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
axes = axes.flatten()

# 创建多边形集合
polygons = []
for element in elements:
    node_indices = element
    polygon = [nodes[node_index] for node_index in node_indices]
    polygons.append(polygon)

# 创建三角形网格
tri = Triangulation([node[0] for node in nodes], [node[1] for node in nodes], triangles=elements)

# 绘制 x 方向位移云图
ax = axes[0]
cmap = 'viridis'
vmin, vmax = min(u_global[::2]), max(u_global[::2])
cf = ax.tripcolor(tri, u_global[::2], shading='gouraud', cmap=cmap, vmin=vmin, vmax=vmax)
ax.set_aspect('equal')
ax.set_xlim(-0.5, 2.5)
ax.set_ylim(-0.5, 1.5)
ax.set_title('x 方向位移云图')
for i, (x, y) in enumerate(nodes):
    ax.text(x, y, f'{u_global[i*2]:.5g}', fontsize=8, ha='center')
fig.colorbar(cf, ax=ax)

# 绘制 y 方向位移云图
ax = axes[1]
vmin, vmax = min(u_global[1::2]), max(u_global[1::2])
cf = ax.tripcolor(tri, u_global[1::2], shading='gouraud', cmap=cmap, vmin=vmin, vmax=vmax)
ax.set_aspect('equal')
ax.set_xlim(-0.5, 2.5)
ax.set_ylim(-0.5, 1.5)
ax.set_title('y 方向位移云图')
for i, (x, y) in enumerate(nodes):
    ax.text(x, y, f'{u_global[i*2+1]:.5g}', fontsize=8, ha='center')
fig.colorbar(cf, ax=ax)

# 绘制 σx 应力云图
ax = axes[2]
vmin, vmax = min(node_stress_avg[:, 0]), max(node_stress_avg[:, 0])
cf = ax.tripcolor(tri, node_stress_avg[:, 0], shading='gouraud', cmap=cmap, vmin=vmin, vmax=vmax)
ax.set_aspect('equal')
ax.set_xlim(-0.5, 2.5)
ax.set_ylim(-0.5, 1.5)
ax.set_title('σx 应力云图')
for i, (x, y) in enumerate(nodes):
    ax.text(x, y, f'{node_stress_avg[i][0]:.5g}', fontsize=8, ha='center')
fig.colorbar(cf, ax=ax)

# 绘制 σy 应力云图
ax = axes[3]
vmin, vmax = min(node_stress_avg[:, 1]), max(node_stress_avg[:, 1])
cf = ax.tripcolor(tri, node_stress_avg[:, 1], shading='gouraud', cmap=cmap, vmin=vmin, vmax=vmax)
ax.set_aspect('equal')
ax.set_xlim(-0.5, 2.5)
ax.set_ylim(-0.5, 1.5)
ax.set_title('σy 应力云图')
for i, (x, y) in enumerate(nodes):
    ax.text(x, y, f'{node_stress_avg[i][1]:.5g}', fontsize=8, ha='center')
fig.colorbar(cf, ax=ax)

# 绘制 τxy 剪切应力云图
ax = axes[4]
vmin, vmax = min(node_stress_avg[:, 2]), max(node_stress_avg[:, 2])
cf = ax.tripcolor(tri, node_stress_avg[:, 2], shading='gouraud', cmap=cmap, vmin=vmin, vmax=vmax)
ax.set_aspect('equal')
ax.set_xlim(-0.5, 2.5)
ax.set_ylim(-0.5, 1.5)
ax.set_title('τxy 剪切应力云图')
for i, (x, y) in enumerate(nodes):
    ax.text(x, y, f'{node_stress_avg[i][2]:.5g}', fontsize=8, ha='center')
fig.colorbar(cf, ax=ax)

# 设置字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号
plt.tight_layout()

# 保存图像
plt.savefig('cloud_plots.png')


# 非阻塞显示图像
plt.show()







