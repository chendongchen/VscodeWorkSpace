import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# 读取文件内容
def read_and_process_data(filename):
    data = []
    with open(filename, 'r') as file:
        for i, line in enumerate(file, 1):
            # 跳过行数为25倍数的行
            if i % 25 == 0:
                continue
            
            # 解析数据行
            if line.startswith('sharink:'):
                # 提取收缩率数值
                parts = line.split()
                shrink_value = float(parts[1])
                data.append(shrink_value)
    
    return data

# 定义拟合函数
def linear_func(x, a, b):
    return a * x + b

def quadratic_func(x, a, b, c):
    return a * x**2 + b * x + c


# 计算相关系数R²
def calculate_r_squared(y_true, y_pred):
    residuals = y_true - y_pred
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((y_true - np.mean(y_true))**2)
    r_squared = 1 - (ss_res / ss_tot)
    return r_squared

# 绘制图表
def plot_shrink_data(data):
    # 修改：每24行为一年，从0年开始计算年份
    years = [(i // 24) + (i % 24) / 24 for i in range(len(data))]
    
    plt.figure(figsize=(15, 8))
    plt.plot(years, data, marker='o', linestyle='-', markersize=3, label='Original Data')
    
    # 进行拟合
    x_data = np.array(years)
    y_data = np.array(data)
    
    # 直线拟合
    popt_linear, _ = curve_fit(linear_func, x_data, y_data)
    y_linear = linear_func(x_data, *popt_linear)
    r2_linear = calculate_r_squared(y_data, y_linear)
    linear_expr = f'y = {popt_linear[0]:.8f}x + {popt_linear[1]:.8f} (R²={r2_linear:.4f})'
    print(f"线性拟合: {linear_expr}")
    plt.plot(years, y_linear, linestyle='--', label=f'Linear Fit: {linear_expr}')
    
    # 二次拟合
    popt_quad, _ = curve_fit(quadratic_func, x_data, y_data)
    y_quad = quadratic_func(x_data, *popt_quad)
    r2_quad = calculate_r_squared(y_data, y_quad)
    quad_expr = f'y = {popt_quad[0]:.8f}x² + {popt_quad[1]:.8f}x + {popt_quad[2]:.8f} (R²={r2_quad:.4f})'
    print(f"二次拟合: {quad_expr}")
    plt.plot(years, y_quad, linestyle='-.', label=f'Quadratic Fit: {quad_expr}')
    
    
    # 设置横坐标为每5年一个标记
    xticks = list(range(0, int(max(years))+1, 5))
    plt.xticks(xticks)
    
    plt.xlabel('Years')
    plt.ylabel('Shrink Rate')
    plt.title('Shrink Rate Over Time with Fitting Curves')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 显示图表
    plt.tight_layout()
    plt.pause(0.001)  # 非阻塞显示

# 计算并绘制数据点间增量图表
def plot_shrink_increment(data):
    # 计算相邻数据点之间的增量
    increments = [0]  # 第一个数据点的增量设为0
    for i in range(1, len(data)):
        increment = data[i] - data[i-1]
        increments.append(increment)
    
    # 修改：每24行为一年，从0年开始计算年份用于x轴
    years = [(i // 24) + (i % 24) / 24 for i in range(len(increments))]
    
    # 绘制增量点线图
    plt.figure(figsize=(15, 8))
    plt.plot(years, increments, marker='o', linestyle='-', markersize=3)
    
    # 设置横坐标为每5年一个标记
    xticks = list(range(0, int(max(years))+1, 5))
    plt.xticks(xticks)
    
    plt.xlabel('Years')
    plt.ylabel('Shrink Rate Increment')
    plt.title('Shrink Rate Increment Between Consecutive Data Points')
    plt.grid(True, alpha=0.3)
    
    # 显示图表
    plt.tight_layout()
    plt.pause(0.001)  # 非阻塞显示

# 主程序
if __name__ == "__main__":
    # 启用交互模式实现非阻塞绘图
    plt.ion()
    
    filename = r"d:\VscodeWorkSpace\H9shrink.txt"
    shrink_data = read_and_process_data(filename)
    plot_shrink_data(shrink_data)
    plot_shrink_increment(shrink_data)
    
    # 保持图形窗口开启
    plt.ioff()  # 关闭交互模式
    plt.show()  # 阻塞显示直到用户关闭窗口
