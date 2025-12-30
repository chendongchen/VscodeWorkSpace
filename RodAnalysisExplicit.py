import numpy as np
import matplotlib.pyplot as plt

def solve_rod_explicit():
    """
    使用显式时间积分方法求解一维变截面圆杆受力问题
    """
    
    # 空间离散化参数
    n_nodes = 5  # 节点数
    L = 1.0      # 杆长度 (m)
    dx = L / (n_nodes - 1)  # 空间步长
    
    # 时间离散化参数
    dt = 1e-6    # 时间步长 (s)
    t_max = 0.001  # 总计算时间 (s)
    n_steps = int(t_max / dt)
    
    # 材料和几何参数
    E = 200e9    # 弹性模量 (Pa)
    rho = 7800   # 密度 (kg/m³)
    P = 1000.0   # 右端拉力 (N)
    
    # 节点位置和直径 (线性变化)
    x = np.linspace(0, L, n_nodes)
    d_left = 0.01    # 左端直径 (m)
    d_right = 0.05   # 右端直径 (m)
    diameters = np.linspace(d_left, d_right, n_nodes)
    areas = np.pi * (diameters/2)**2  # 各节点截面积
    
    # 质量矩阵计算 (使用集中质量法)
    masses = np.zeros(n_nodes)
    for i in range(n_nodes):
        if i == 0:  # 第一个节点
            volumes = (areas[i] + areas[i+1]) * dx / 2
        elif i == n_nodes-1:  # 最后一个节点
            volumes = (areas[i-1] + areas[i]) * dx / 2
        else:  # 中间节点
            volumes = (areas[i-1] + 2*areas[i] + areas[i+1]) * dx / 4
        masses[i] = rho * volumes
    
    # 初始化位移、速度和加速度
    u = np.zeros(n_nodes)      # 位移
    v = np.zeros(n_nodes)      # 速度
    a = np.zeros(n_nodes)      # 加速度
    
    # 显式求解过程
    print("开始显式时间积分求解...")
    print(f"时间步长: {dt:.2e} s")
    print(f"总时间步数: {n_steps}")
    
    # 存储特定节点的位移历史用于绘图
    node_hist = 2  # 观察中间节点
    time_history = []
    displacement_history = []
    
    # 时间步进循环
    for step in range(n_steps):
        t = step * dt
        
        # 计算内部力 (使用中心差分格式)
        internal_force = np.zeros(n_nodes)
        
        # 内部节点 (1 到 n_nodes-2)
        for i in range(1, n_nodes-1):
            # 左侧应力
            strain_left = (u[i] - u[i-1]) / dx
            stress_left = E * strain_left
            area_left = (areas[i] + areas[i-1]) / 2
            force_left = stress_left * area_left
            
            # 右侧应力
            strain_right = (u[i+1] - u[i]) / dx
            stress_right = E * strain_right
            area_right = (areas[i] + areas[i+1]) / 2
            force_right = stress_right * area_right
            
            # 节点内力平衡
            internal_force[i] = force_right - force_left
        
        # 边界条件处理
        # 左端固定 (节点0)
        internal_force[0] = 0
        u[0] = 0
        v[0] = 0
        
        # 右端受力 (节点n_nodes-1)
        strain_right_end = (u[n_nodes-1] - u[n_nodes-2]) / dx
        stress_right_end = E * strain_right_end
        area_right_end = (areas[n_nodes-2] + areas[n_nodes-1]) / 2
        force_right_end = stress_right_end * area_right_end
        internal_force[n_nodes-1] = P - force_right_end  # 外力减去内力
        
        # 计算加速度 (牛顿第二定律: F = ma)
        for i in range(n_nodes):
            a[i] = internal_force[i] / masses[i]
        
        # 更新速度和位移 (显式欧拉格式)
        for i in range(n_nodes):
            v[i] = v[i] + a[i] * dt
            u[i] = u[i] + v[i] * dt
        
        # 记录历史数据
        if step % 100 == 0:  # 每100步记录一次
            time_history.append(t)
            displacement_history.append(u[node_hist])
            
        # 显示进度
        if step % (n_steps // 10) == 0:
            print(f"计算进度: {step/n_steps*100:.1f}%")
    
    print("计算完成!")
    
    # 计算最终轴力分布
    forces = np.zeros(n_nodes-1)
    for i in range(n_nodes-1):
        strain = (u[i+1] - u[i]) / dx
        stress = E * strain
        area = (areas[i] + areas[i+1]) / 2
        forces[i] = stress * area
    
    return x, diameters, u, forces, areas, time_history, displacement_history

def plot_explicit_results(x, diameters, displacements, forces, areas, time_history, displacement_history):
    """绘制显式求解结果"""
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    
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
    x_forces = (x[:-1] + x[1:]) / 2
    ax3.plot(x_forces, forces/1000, 'go-', label='轴力')
    ax3.set_ylabel('轴力 (kN)')
    ax3.set_xlabel('位置 (m)')
    ax3.grid(True)
    ax3.set_title('轴力分布')
    ax3.legend()
    
    # 绘制时间历程
    ax4.plot(time_history, np.array(displacement_history)*1e6, 'm-')
    ax4.set_xlabel('时间 (s)')
    ax4.set_ylabel('位移 (μm)')
    ax4.grid(True)
    ax4.set_title('中间节点位移时间历程')
    
    plt.tight_layout()
    plt.show()

def print_explicit_analysis():
    """打印显式分析过程说明"""
    print("一维变截面圆杆受力分析 - 显式时间积分法")
    print("=" * 50)
    print("求解方法:")
    print("- 采用显式时间积分方法")
    print("- 使用中心差分格式计算应变和应力")
    print("- 应用牛顿第二定律计算节点加速度")
    print("- 通过欧拉方法更新速度和位移")
    print()
    print("差分方程:")
    print("- 位移更新: u^{n+1} = u^n + v^n * Δt")
    print("- 速度更新: v^{n+1} = v^n + a^n * Δt")
    print("- 加速度计算: a^n = F^n / m")
    print("- 应力应变关系: σ = E * ε")
    print()

if __name__ == "__main__":
    # 打印分析过程
    print_explicit_analysis()
    
    # 执行显式求解
    x, diameters, displacements, forces, areas, time_history, displacement_history = solve_rod_explicit()
    
    # 输出结果
    print("\n计算结果:")
    print("-" * 30)
    print("节点位置 (m):     ", [f"{val:.2f}" for val in x])
    print("节点直径 (mm):    ", [f"{val*1000:.1f}" for val in diameters])
    print("节点位移 (μm):    ", [f"{val*1e6:.4f}" for val in displacements])
    print("单元轴力 (kN):    ", [f"{val/1000:.2f}" for val in forces])
    
    # 绘制结果
    plot_explicit_results(x, diameters, displacements, forces, areas, time_history, displacement_history)