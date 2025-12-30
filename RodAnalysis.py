import numpy as np
import matplotlib.pyplot as plt

def solve_rod_force_distribution():
    """
    求解一端固定一端受拉的变截面圆杆的内力分布
    
    杆件参数:
    - 长度 L = 1.0 m
    - 分为5个节点(0-4)，即4个单元
    - 左端固定(节点0)，右端受拉力P=1000N
    - 截面直径从左到右线性增加：d0=0.01m 到 d4=0.05m
    - 弹性模量 E = 200GPa
    """
    
    # 基本参数设置
    n_nodes = 5  # 节点数
    L = 1.0      # 杆长度(m)
    P = 1000.0   # 右端受力(N)
    E = 200e9    # 弹性模量(Pa)
    
    # 节点位置和直径
    x = np.linspace(0, L, n_nodes)  # 节点坐标
    d_left = 0.01   # 左端直径(m)
    d_right = 0.05  # 右端直径(m)
    diameters = np.linspace(d_left, d_right, n_nodes)  # 各节点直径
    
    # 计算各段面积
    areas = np.pi * (diameters/2)**2
    
    # 单元长度
    dx = L / (n_nodes - 1)
    
    # 建立差分方程系数矩阵和右端项
    # 对于内部节点，使用差分格式: (EA_{i-1/2}(u_i-u_{i-1})/dx - EA_{i+1/2}(u_{i+1}-u_i)/dx) = 0
    # 其中EA_{i-1/2}表示在x_{i-1/2}处的EA值，近似用相邻两点平均值
    
    # 构建系数矩阵K和载荷向量F
    K = np.zeros((n_nodes, n_nodes))
    F = np.zeros(n_nodes)
    
    # 边界条件处理
    # 左端固定 u[0] = 0
    K[0, 0] = 1.0
    
    # 内部节点差分方程 (节点1, 2, 3)
    for i in range(1, n_nodes-1):
        # 在x_{i-1/2}处的EA值 (单元(i-1,i)之间)
        EA_left = E * np.mean([areas[i-1], areas[i]])
        # 在x_{i+1/2}处的EA值 (单元(i,i+1)之间)
        EA_right = E * np.mean([areas[i], areas[i+1]])
        
        # 差分方程系数
        K[i, i-1] = EA_left / dx**2
        K[i, i] = -(EA_left + EA_right) / dx**2
        K[i, i+1] = EA_right / dx**2
    
    # 右端受力边界条件 (节点4)
    # 在x_{3+1/2}处的EA值
    EA_right_end = E * np.mean([areas[3], areas[4]])
    K[4, 3] = EA_right_end / dx**2
    K[4, 4] = -EA_right_end / dx**2
    F[4] = -P  # 负号是因为力的方向与位移正方向相关
    
    # 求解位移场
    displacements = np.linalg.solve(K, F)
    
    # 计算轴力 (每个单元的内力)
    forces = np.zeros(n_nodes-1)
    for i in range(n_nodes-1):
        EA = E * np.mean([areas[i], areas[i+1]])  # 单元内的平均EA值
        strain = (displacements[i+1] - displacements[i]) / dx
        forces[i] = EA * strain
    
    return x, diameters, displacements, forces, areas

def plot_results(x, diameters, displacements, forces, areas):
    """绘制结果图"""
    
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(10, 12))
    
    # 绘制直径分布
    ax1.plot(x, diameters*1000, 'bo-', label='直径')
    ax1.set_ylabel('直径 (mm)')
    ax1.grid(True)
    ax1.set_title('变截面圆杆几何参数')
    ax1.legend()
    
    # 绘制位移分布
    ax2.plot(x, displacements*1e6, 'ro-', label='位移')
    ax2.set_ylabel('位移 (μm)')
    ax2.grid(True)
    ax2.set_title('节点位移分布')
    ax2.legend()
    
    # 绘制轴力分布
    x_forces = (x[:-1] + x[1:]) / 2  # 力作用在单元中心
    ax3.plot(x_forces, forces/1000, 'go-', label='轴力')
    ax3.set_ylabel('轴力 (kN)')
    ax3.grid(True)
    ax3.set_title('轴力分布')
    ax3.legend()
    
    # 绘制应力分布
    stresses = forces / areas[:-1]
    ax4.plot(x_forces, stresses/1e6, 'mo-', label='应力')
    ax4.set_ylabel('应力 (MPa)')
    ax4.set_xlabel('位置 (m)')
    ax4.grid(True)
    ax4.set_title('应力分布')
    ax4.legend()
    
    plt.tight_layout()
    plt.show()

def print_analysis_process():
    """打印分析过程说明"""
    print("一维变截面圆杆受力分析 - 差分法求解过程")
    print("=" * 50)
    print("问题描述:")
    print("- 杆件长度: 1.0 m")
    print("- 左端固定，右端受拉力 P = 1000 N")
    print("- 截面为圆形，直径从左端10mm线性增加到右端50mm")
    print("- 材料弹性模量 E = 200 GPa")
    print("- 将杆件划分为5个节点(4个单元)")
    print()
    print("差分方程建立过程:")
    print("1. 对每个内部节点应用平衡方程")
    print("2. 使用中心差分格式近似应变")
    print("3. 根据胡克定律 σ = E * ε 计算应力")
    print("4. 根据内力与应力关系 N = σ * A 计算轴力")
    print("5. 考虑变截面特性，在计算EA时采用相邻节点面积平均值")
    print()

if __name__ == "__main__":
    # 打印分析过程
    print_analysis_process()
    
    # 求解差分方程
    x, diameters, displacements, forces, areas = solve_rod_force_distribution()
    
    # 输出结果
    print("计算结果:")
    print("-" * 30)
    print("节点位置 (m):     ", [f"{val:.2f}" for val in x])
    print("节点直径 (mm):    ", [f"{val*1000:.1f}" for val in diameters])
    print("节点面积 (mm²):   ", [f"{val*1e6:.2f}" for val in areas])
    print("节点位移 (μm):    ", [f"{val*1e6:.4f}" for val in displacements])
    print("单元轴力 (kN):    ", [f"{val/1000:.2f}" for val in forces])
    print("单元应力 (MPa):   ", [f"{val/1e6:.2f}" for val in forces / areas[:-1]])
    
    # 绘制结果
    plot_results(x, diameters, displacements, forces, areas)