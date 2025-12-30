import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os

def solve_rod_with_animation():
    """
    Using explicit time integration method to solve 1D variable cross-section circular rod problem with animation
    """
    
    # Spatial discretization parameters
    n_nodes = 50  # Number of nodes
    L = 1.0      # Rod length (m)
    dx = L / (n_nodes - 1)  # Spatial step size
    
    # Material and geometric parameters
    E = 200e9    # Elastic modulus (Pa)
    rho = 7800   # Density (kg/m³)
    P = 10000.0   # Right end tension (N)
    
    # 添加阻尼系数
    damping_coefficient = 1000.0  # 阻尼系数，可根据需要调整
    
    # Calculate time step based on wave speed and minimum geometry
    c = np.sqrt(E / rho)  # Wave speed
    dt = 0.8 * dx / c     # CFL condition for stability with safety factor
    t_max = 0.5         # Increase total time to ensure convergence
    n_steps = int(t_max / dt)
    # 修改: 固定每100步记录一次动画帧
    frame_interval = 100  # Record every 100 steps
    
    # Node positions and diameters (linear variation)
    x = np.linspace(0, L, n_nodes)
    d_left = 0.01    # Left end diameter (m)
    d_right = 0.05   # Right end diameter (m)
    diameters = np.linspace(d_left, d_right, n_nodes)
    areas = np.pi * (diameters/2)**2  # Cross-sectional area at each node
    
    # Mass matrix calculation (using lumped mass method)
    masses = np.zeros(n_nodes)
    for i in range(n_nodes):
        if i == 0:  # First node
            volumes = (areas[i] + areas[i+1]) * dx / 2
        elif i == n_nodes-1:  # Last node
            volumes = (areas[i-1] + areas[i]) * dx / 2
        else:  # Intermediate nodes
            volumes = (areas[i-1] + 2*areas[i] + areas[i+1]) * dx / 4
        masses[i] = rho * volumes
    
    # Initialize displacement, velocity and acceleration
    u = np.zeros(n_nodes)      # Displacement
    v = np.zeros(n_nodes)      # Velocity
    a = np.zeros(n_nodes)      # Acceleration
    
    # Create animation figure
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('1D Variable Cross-Section Circular Rod Analysis - Explicit Solution Animation', fontsize=14)
    
    # Prepare animation data storage
    animation_data = {
        'times': [],
        'displacements': [],
        'forces': [],
        'step_numbers': [],
        'unbalanced_forces': []  # Store unbalanced forces for monitoring
    }
    
    print("Starting explicit time integration solution...")
    print(f"Time step: {dt:.2e} s (based on wave speed and CFL condition)")
    print(f"Total time steps: {n_steps}")
    # 修改: 更新提示信息
    print(f"Animation frame interval: Record every {frame_interval} steps")
    print(f"Damping coefficient: {damping_coefficient:.1f} N·s/m")
    
    # Time stepping loop
    convergence_reached = False
    # 新增: 定义收敛限制条件
    convergence_limit = 1e-5
    initial_unbalanced_force = None  # 用于存储初始不平衡力
    
    for step in range(n_steps):
        t = step * dt
        
        # Calculate internal forces (using central difference scheme)
        internal_force = np.zeros(n_nodes)
        
        # Internal nodes (1 to n_nodes-2)
        for i in range(1, n_nodes-1):
            # Left stress
            strain_left = (u[i] - u[i-1]) / dx
            stress_left = E * strain_left
            area_left = (areas[i] + areas[i-1]) / 2
            force_left = stress_left * area_left
            
            # Right stress
            strain_right = (u[i+1] - u[i]) / dx
            stress_right = E * strain_right
            area_right = (areas[i] + areas[i+1]) / 2
            force_right = stress_right * area_right
            
            # Node internal force balance
            internal_force[i] = force_right - force_left
        
        # Boundary condition processing
        # Left end fixed (node 0)
        internal_force[0] = 0
        u[0] = 0
        v[0] = 0
        
        # Right end loaded (node n_nodes-1)
        strain_right_end = (u[n_nodes-1] - u[n_nodes-2]) / dx
        stress_right_end = E * strain_right_end
        area_right_end = (areas[n_nodes-2] + areas[n_nodes-1]) / 2
        force_right_end = stress_right_end * area_right_end
        internal_force[n_nodes-1] = P - force_right_end  # External force minus internal force
        
        # 添加阻尼力计算 (与速度成正比，方向相反)
        damping_force = damping_coefficient * v
        
        # Calculate unbalanced force for convergence check (including damping force)
        unbalanced_forces = np.abs(internal_force - damping_force)
        max_unbalanced_force = np.max(unbalanced_forces)
        
        # 新增: 记录初始不平衡力
        if initial_unbalanced_force is None:
            initial_unbalanced_force = max_unbalanced_force
        
        # Check convergence (stop when all unbalanced forces < 1e-5)
        if max_unbalanced_force < convergence_limit:
            convergence_reached = True
            print(f"Convergence reached at step {step}, max unbalanced force: {max_unbalanced_force:.2e}")
        
        # Calculate acceleration (Newton's second law: F = ma, including damping)
        for i in range(n_nodes):
            # 总力 = 内力 - 阻尼力
            total_force = internal_force[i] - damping_force[i]
            a[i] = total_force / masses[i]
        
        # Update velocity and displacement (explicit Euler scheme)
        for i in range(n_nodes):
            v[i] = v[i] + a[i] * dt
            u[i] = u[i] + v[i] * dt
        
        # Record animation data
        # 修改: 每100步记录一次或者收敛时记录
        if step % frame_interval == 0 or convergence_reached:
            # Calculate current axial force distribution
            forces = np.zeros(n_nodes-1)
            strains = np.zeros(n_nodes-1)
            stresses = np.zeros(n_nodes-1)
            
            for i in range(n_nodes-1):
                strain = (u[i+1] - u[i]) / dx
                stress = E * strain
                area = (areas[i] + areas[i+1]) / 2
                force = stress * area
                
                strains[i] = strain
                stresses[i] = stress
                forces[i] = force
            
            animation_data['times'].append(t)
            animation_data['displacements'].append(u.copy())
            animation_data['forces'].append(forces.copy())
            animation_data['step_numbers'].append(step)
            animation_data['unbalanced_forces'].append(unbalanced_forces.copy())
            
            # 修改: 每100步输出一次进度，使用不平衡力与限制条件比值的倒数显示进度
            if step % frame_interval == 0:
                # 计算进度指标：初始不平衡力与当前不平衡力的比值
                progress_ratio = np.log(convergence_limit/ max_unbalanced_force)
                print(f"Calculation progress: ratio={progress_ratio:.1f}, Max unbalanced force: {max_unbalanced_force:.2e}")
        
        # Stop iteration if convergence is reached
        if convergence_reached:
            break
    
    print("Calculation completed! Generating plots...")
    print(f"Final step: {len(animation_data['times'])-1}, Final time: {animation_data['times'][-1]:.4f}s")
    
    # Animation initialization function
    def init():
        # Draw fixed geometric information
        ax1.clear()
        ax1.plot(x, diameters*1000, 'bo-', linewidth=2, markersize=6)
        ax1.set_ylabel('Diameter (mm)')
        ax1.grid(True)
        ax1.set_title('Variable Cross-Section Rod Geometry')
        
        return []
    
    # Animation update function
    def update(frame):
        # Clear previous plots
        ax2.clear()
        ax3.clear()
        ax4.clear()
        
        time = animation_data['times'][frame]
        displacements = animation_data['displacements'][frame]
        forces = animation_data['forces'][frame]
        step_num = animation_data['step_numbers'][frame]
        unbalanced = animation_data['unbalanced_forces'][frame]
        
        # Plot displacement distribution
        ax2.plot(x, displacements*1e6, 'ro-', linewidth=2, markersize=6)
        ax2.set_ylabel('Displacement (μm)')
        ax2.set_xlabel('Position (m)')  # 添加x轴标签
        ax2.grid(True)
        ax2.set_title(f'Node Displacement Distribution (Time: {time*1000:.2f} ms, Step: {step_num})')
        
        # Plot axial force distribution
        x_forces = (x[:-1] + x[1:]) / 2
        ax3.plot(x_forces, forces/1000, 'go-', linewidth=2, markersize=6)
        ax3.set_ylabel('Axial Force (kN)')
        ax3.set_xlabel('Position (m)')  # 添加x轴标签
        ax3.grid(True)
        ax3.set_title('Axial Force Distribution')
        
        # Plot maximum displacement and unbalanced force history
        times_so_far = animation_data['times'][:frame+1]
        max_displacements = [np.max(np.abs(disp)) for disp in animation_data['displacements'][:frame+1]]
        max_unbalanced_history = [np.max(uf) for uf in animation_data['unbalanced_forces'][:frame+1]]
        
        ax4.plot(times_so_far, np.array(max_displacements)*1e6, 'b-', linewidth=2, label='Max Displacement')
        ax4.set_xlabel('Time (s)')
        ax4.set_ylabel('Maximum Displacement (μm)', color='b')
        ax4.grid(True)
        
        # Add secondary y-axis for unbalanced forces
        ax4_twin = ax4.twinx()
        ax4_twin.plot(times_so_far, max_unbalanced_history, 'r--', linewidth=2, label='Max Unbalanced Force')
        ax4_twin.set_ylabel('Max Unbalanced Force (N)', color='r')
        ax4_twin.set_yscale('log')
        
        ax4.set_title('Maximum Displacement and Unbalanced Force History')
        
        return []
    
    # 创建保存动画的子文件夹
    animation_folder = "rod_analysis_animations"
    if not os.path.exists(animation_folder):
        os.makedirs(animation_folder)
    
    # 保存每张子图为单独的文件
    final_frame = len(animation_data['times']) - 1
    update(final_frame)  # 更新到最后一帧
    
    # 保存每个子图
    fig.savefig(os.path.join(animation_folder, "rod_analysis_all_subplots.png"), dpi=300, bbox_inches='tight')
    
    # 分别保存每个子图
    extents = ax1.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    fig.savefig(os.path.join(animation_folder, "rod_geometry.png"), dpi=300, bbox_inches=extents)
    
    extents = ax2.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    fig.savefig(os.path.join(animation_folder, "rod_displacement.png"), dpi=300, bbox_inches=extents)
    
    extents = ax3.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    fig.savefig(os.path.join(animation_folder, "rod_axial_force.png"), dpi=300, bbox_inches=extents)
    
    extents = ax4.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    fig.savefig(os.path.join(animation_folder, "rod_displacement_history.png"), dpi=300, bbox_inches=extents)
    
    print("Individual subplots saved as PNG files.")
    
    # 新增：绘制并保存位移、轴力、不平衡力随时间的变化曲线
    # 计算每个时间点的最大位移、最大轴力和最大不平衡力
    max_displacements = [np.max(np.abs(disp)) for disp in animation_data['displacements']]
    max_forces = [np.max(np.abs(force)) for force in animation_data['forces']]
    max_unbalanced_forces = [np.max(uf) for uf in animation_data['unbalanced_forces']]
    
    # 创建新的图形来显示这些时间历程数据
    fig2, (ax_disp, ax_force, ax_unbal) = plt.subplots(3, 1, figsize=(10, 12))
    
    # 绘制位移随时间变化
    ax_disp.plot(animation_data['times'], np.array(max_displacements)*1e6, 'b-', linewidth=2)
    ax_disp.set_xlabel('Time (s)')
    ax_disp.set_ylabel('Maximum Displacement (μm)')
    ax_disp.set_title('Maximum Displacement vs Time')
    ax_disp.grid(True)
    
    # 绘制轴力随时间变化
    ax_force.plot(animation_data['times'], np.array(max_forces)/1000, 'g-', linewidth=2)
    ax_force.set_xlabel('Time (s)')
    ax_force.set_ylabel('Maximum Axial Force (kN)')
    ax_force.set_title('Maximum Axial Force vs Time')
    ax_force.grid(True)
    
    # 绘制不平衡力随时间变化
    ax_unbal.plot(animation_data['times'], max_unbalanced_forces, 'r-', linewidth=2)
    ax_unbal.set_xlabel('Time (s)')
    ax_unbal.set_ylabel('Maximum Unbalanced Force (N)')
    ax_unbal.set_title('Maximum Unbalanced Force vs Time')
    ax_unbal.set_yscale('log')
    ax_unbal.grid(True)
    
    plt.tight_layout()
    fig2.savefig(os.path.join(animation_folder, "time_history_curves.png"), dpi=300, bbox_inches='tight')
    plt.close(fig2)
    
    print("Time history curves saved as PNG file.")
    
    return animation_data

def print_animation_info():
    """Print animation related information"""
    print("1D Variable Cross-Section Rod Force Analysis - Animation Demo")
    print("=" * 50)
    print("Animation Demo Content:")
    print("- Real-time display of rod deformation process")
    print("- Display of axial force distribution changes")
    print("- Show maximum displacement development over time")
    print("- Monitor convergence based on unbalanced forces")
    print()
    print("Explicit Solution Features:")
    print("- Each time step is calculated independently, no need to solve linear equations")
    print("- Visualization of calculation process for better understanding of physical phenomena")
    print("- Can observe dynamic effects such as wave propagation")
    print("- Automatic time step calculation based on wave speed")
    print("- Convergence checking using unbalanced force criteria (< 1e-5 N)")
    print()

if __name__ == "__main__":
    # Print animation information
    print_animation_info()
    
    # Execute explicit solution with animation
    data = solve_rod_with_animation()