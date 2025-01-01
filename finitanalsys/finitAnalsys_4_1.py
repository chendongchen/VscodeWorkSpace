# 陈东 2024-11-30日，于国科大雁栖湖校区编写
# 有限元分析作业 作业4第1题 学号202418000531019 班级序号：24
# 运行结果保存到 位移与应力云图./cloud_plots.png 整体刚度矩阵保存到 ./global_stiffness_matrix.xlsx

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.tri import Triangulation

E = 210e9  # 弹性模量，单位 Pa
nu = 0.2  # 泊松比
t = 0.01  # 厚度，单位 m
q = 1e6  # 载荷kN/m
f = t * q 
size_nodes_finit = 100 # 节点密度 单位1/m

# 用户定义节点和单元
def generate_nodes_and_elements_size(num_nodes_size):
    """
    生成给定节点数量的网格的节点和单元信息。

    参数:
    num_nodes_size (int): 网格中节点的数量。

    返回:
    tuple: 包含两个列表，第一个列表是节点坐标，第二个列表是单元节点索引。
    """
    num_rows = num_nodes_size
    num_nodes_per_row = num_nodes_size
    nodes = []
    elements = []
    
    # 生成节点
    for row in range(num_rows):
        for col in range(num_nodes_per_row+row):
            nodes.append((col/(num_nodes_size-1), 1-row/(num_nodes_size-1)))
    
    # 生成单元
    nodes_index = 0
    for row in range(num_rows - 1):
        if row%2 == 0:
            for col in range(num_nodes_per_row +row - 1):
                elements.append([nodes_index//2, nodes_index//2 + num_nodes_per_row +row, nodes_index//2 + num_nodes_per_row +row + 1])
                elements.append([nodes_index//2, nodes_index//2 + num_nodes_per_row +row + 1, nodes_index//2 + 1])
                nodes_index = nodes_index + 2
            elements.append([nodes_index//2, nodes_index//2 + num_nodes_per_row +row, nodes_index//2 + num_nodes_per_row +row + 1])
            nodes_index = nodes_index + 1
        else:
            for col in range(num_nodes_per_row +row - 1):
                nodes_index = nodes_index + 1
                elements.append([nodes_index//2, nodes_index//2 + num_nodes_per_row +row, nodes_index//2 + num_nodes_per_row +row + 1])
                elements.append([nodes_index//2, nodes_index//2 + num_nodes_per_row +row + 1, nodes_index//2 + 1])
                nodes_index = nodes_index + 1
            nodes_index = nodes_index + 1    
            elements.append([nodes_index//2, nodes_index//2 + num_nodes_per_row +row, nodes_index//2 + num_nodes_per_row +row + 1])
            nodes_index = nodes_index + 2
            
    
    return nodes, elements

def get_indices_of_free_dofs(nodes_zies):
    """
    计算并返回所有自由节点的自由度（DOF）索引列表。
    
    该函数假定网格为正方形网格，且底边节点固定。每个节点有两个自由度（例如，x和y方向的位移）。
    
    参数:
    nodes_zies (int): 每边的节点数。
    
    返回:
    list: 自由节点的自由度索引列表。
    """

    num_nodes_per_row = nodes_zies
    num_rows = nodes_zies
    dof_indices = []
        # 生成节点
    i = 0
    for row in range(num_rows-1):   #底边固定
        for col in range(num_nodes_per_row+row):
            dof_indices.append(i*2)
            dof_indices.append(i*2+1)
            i = i + 1

    return dof_indices

def show_plots(nodes, elements) :
    """
    绘制并展示三角网格图形。

    参数:
    nodes: 节点坐标列表，每个节点由一对X和Y坐标组成。
    elements: 元素列表，每个元素由三个节点索引组成，表示一个三角形。

    返回值:
    无返回值，但会保存并展示三角网格图形。
    """
    # 绘制三角网格
    x, y = zip(*nodes)
    triangles = elements

    fig, ax = plt.subplots()
    ax.triplot(x, y, triangles, 'b-', lw=1)
    ax.set_title('Triangular Grid')
    plt.xlabel('X coordinate')
    plt.ylabel('Y coordinate')
    plt.grid(True)
    # 保存图像
    plt.savefig('mesh_grid'+str(size_nodes_finit)+'.png')
    plt.show()

def calculate_area(x1, y1, x2, y2, x3, y3):
    return 0.5 * abs(x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1 - y2))

def calculate_stiffness_matrix(x1, y1, x2, y2, x3, y3, E, nu, t):
    """
    计算刚度矩阵 K。
    
    参数:
    x1, y1, x2, y2, x3, y3 -- 三角形节点坐标
    E -- 杨氏模量
    nu -- 泊松比
    t -- 板厚
    
    返回:
    K -- 刚度矩阵
    B -- 形状函数导数矩阵
    D -- 弹性矩阵
    """
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
    """
    组装全局刚度矩阵

    参数:
    elements: 元素连接表，每个元素由节点索引组成
    nodes: 节点坐标表，每个节点由其坐标组成
    E: 杨氏模量
    nu: 泊松比
    t: 板的厚度

    返回:
    global_K: 全局刚度矩阵
    """
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

def plot_results(nodes, elements, u_global, node_stress_avg, size_nodes_finit):
    """
    绘制并保存位移和应力云图。

    参数:
    nodes: 节点坐标列表，每个节点由一对X和Y坐标组成。
    elements: 元素列表，每个元素由三个节点索引组成，表示一个三角形。
    u_global: 整体节点位移向量。
    node_stress_avg: 每个节点的平均应力。
    size_nodes_finit: 节点密度。

    返回值:
    无返回值，但会保存并展示云图。
    """
    # 创建三角形网格
    tri = Triangulation([node[0] for node in nodes], [node[1] for node in nodes], triangles=elements)

    # 绘制云图
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    axes = axes.flatten()

    # 绘制 x 方向位移云图
    ax = axes[0]
    cmap = 'viridis'
    vmin, vmax = min(u_global[::2]), max(u_global[::2])
    cf = ax.tripcolor(tri, u_global[::2], shading='gouraud', cmap=cmap, vmin=vmin, vmax=vmax)
    ax.set_aspect('equal')
    ax.set_xlim(-0.5, 2.5)
    ax.set_ylim(-0.5, 1.5)
    ax.set_title('x 方向位移云图')
    fig.colorbar(cf, ax=ax)

    # 绘制 y 方向位移云图
    ax = axes[1]
    vmin, vmax = min(u_global[1::2]), max(u_global[1::2])
    cf = ax.tripcolor(tri, u_global[1::2], shading='gouraud', cmap=cmap, vmin=vmin, vmax=vmax)
    ax.set_aspect('equal')
    ax.set_xlim(-0.5, 2.5)
    ax.set_ylim(-0.5, 1.5)
    ax.set_title('y 方向位移云图')
    fig.colorbar(cf, ax=ax)

    # 绘制 σx 应力云图
    ax = axes[2]
    vmin, vmax = min(node_stress_avg[:, 0]), max(node_stress_avg[:, 0])
    cf = ax.tripcolor(tri, node_stress_avg[:, 0], shading='gouraud', cmap=cmap, vmin=vmin, vmax=vmax)
    ax.set_aspect('equal')
    ax.set_xlim(-0.5, 2.5)
    ax.set_ylim(-0.5, 1.5)
    ax.set_title('σx 应力云图')
    fig.colorbar(cf, ax=ax)

    # 绘制 σy 应力云图
    ax = axes[3]
    vmin, vmax = min(node_stress_avg[:, 1]), max(node_stress_avg[:, 1])
    cf = ax.tripcolor(tri, node_stress_avg[:, 1], shading='gouraud', cmap=cmap, vmin=vmin, vmax=vmax)
    ax.set_aspect('equal')
    ax.set_xlim(-0.5, 2.5)
    ax.set_ylim(-0.5, 1.5)
    ax.set_title('σy 应力云图')
    fig.colorbar(cf, ax=ax)

    # 绘制 τxy 剪切应力云图
    ax = axes[4]
    vmin, vmax = min(node_stress_avg[:, 2]), max(node_stress_avg[:, 2])
    cf = ax.tripcolor(tri, node_stress_avg[:, 2], shading='gouraud', cmap=cmap, vmin=vmin, vmax=vmax)
    ax.set_aspect('equal')
    ax.set_xlim(-0.5, 2.5)
    ax.set_ylim(-0.5, 1.5)
    ax.set_title('τxy 剪切应力云图')
    fig.colorbar(cf, ax=ax)

    # 设置字体
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
    plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号
    plt.tight_layout()

    # 保存图像
    plt.savefig('cloud_plots' + str(size_nodes_finit) + '.png')

    # 非阻塞显示图像
    plt.show()

# 主程序
nodes, elements = generate_nodes_and_elements_size(size_nodes_finit)
show_plots(nodes, elements)
dof_indices = get_indices_of_free_dofs(size_nodes_finit)
F = np.array([f] + [0] * (len(dof_indices) - 1))

global_K = assemble_global_stiffness_matrix(elements, nodes, E, nu, t)
# print(global_K)    # 打印刚度矩阵


# # 将刚度矩阵保存为 Excel 文件
# df = pd.DataFrame(global_K)
# df.to_excel('global_stiffness_matrix'+str(size_nodes_finit)+'.xlsx', index=False, header=False)

# print("刚度矩阵已保存到 global_stiffness_matrix"+str(size_nodes_finit)+".xlsx")


reduced_K = global_K[np.ix_(dof_indices, dof_indices)]

# print("\n与节点 0 和 1 有关的刚度矩阵:")
# print(reduced_K)


# 求解线性方程组
u = np.linalg.solve(reduced_K, F)

# print("\n节点  的位移:")
# print(u)

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

# 创建一个包含节点坐标、位移、应力和力的DataFrame
data = {
    'Node Index': list(range(len(nodes))),
    'X Coordinate': [node[0] for node in nodes],
    'Y Coordinate': [node[1] for node in nodes],
    'Displacement X': u_global[::2],
    'Displacement Y': u_global[1::2],
    'Stress X': node_stress_avg[:, 0],
    'Stress Y': node_stress_avg[:, 1],
    'Shear Stress XY': node_stress_avg[:, 2],
    'Force X': F_total[::2],
    'Force Y': F_total[1::2]
}

df_combined = pd.DataFrame(data)

# 将DataFrame保存到Excel文件中
df_combined.to_excel('combined_results'+str(size_nodes_finit)+'.xlsx', index=False)

print(f"综合结果已保存到 combined_results{size_nodes_finit}.xlsx")

# 绘制云图
# 调用绘图函数
plot_results(nodes, elements, u_global, node_stress_avg, size_nodes_finit)







