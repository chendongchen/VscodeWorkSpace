import numpy as np
import matplotlib.pyplot as plt
import re
from scipy.optimize import curve_fit
from read_and_plot import read_and_process_data

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 解析数据
filename = r"D:\VscodeWorkSpace\H9shrink.txt"
shrink_data = read_and_process_data(filename)

# 构造counts数组（每行对应一个count），单位为半个月
counts = np.arange(1, len(shrink_data) + 1)
sharink = np.array(shrink_data)

# 定义拟合函数（对数增长模型，符合数据饱和趋势）
def logistic_func(x, a, x0, k, d): 
    """4-参数逻辑增长模型：a/(1 + exp(-k*(x-x0))) + d
    参数:
    - a: 振幅 (上限 - 下限)
    - x0: 中点 (counts 的中位位置)
    - k: 斜率/增长率
    - d: 下限/偏移
    采用标准形式可以避免参数退化（a 和 d 互相抵消）并便于设定 bounds
    """
    return a / (1 + np.exp(-k * (x - x0))) + d

# 拟合数据
# 对 x 做标准化可以提高拟合的数值稳定性
counts_min, counts_max = counts.min(), counts.max()
counts_scaled = (counts - counts_min) / (counts_max - counts_min)

# 初始参数估计: a ~ 振幅, x0 ~ 中心(标准化范围0..1), k ~ 增长率(正), d ~ 最小值
p0 = [sharink.max() - sharink.min(), 0.5, 0.02, sharink.min()]
lower_bounds = [0.0, 0.0, 1e-6, sharink.min() - 0.1]
upper_bounds = [1.0, 1.0, 10.0, sharink.max() + 0.1]

# 计算相关系数R²
def calculate_r_squared(y_true, y_pred):
    residuals = y_true - y_pred
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((y_true - np.mean(y_true))**2)
    r_squared = 1 - (ss_res / ss_tot)
    return r_squared

try:
    popt, pcov = curve_fit(logistic_func, counts_scaled, sharink, p0=p0, bounds=(lower_bounds, upper_bounds), maxfev=200000)
    fitted_sharink = logistic_func(counts_scaled, *popt)
    r_squared = calculate_r_squared(sharink, fitted_sharink)
    print('拟合成功: popt =', popt)
except Exception as e:
    # 如果拟合失败，尝试一些容错策略：放宽 bounds 或增加 maxfev
    print('初次拟合失败，错误:', e)
    try:
        popt, pcov = curve_fit(logistic_func, counts_scaled, sharink, p0=p0, maxfev=500000)
        fitted_sharink = logistic_func(counts_scaled, *popt)
        r_squared = calculate_r_squared(sharink, fitted_sharink)
        print('第二次拟合成功: popt =', popt)
    except Exception as e2:
        print('拟合仍然失败，跳过拟合并使用原始数据绘图。错误:', e2)
        popt = None
        fitted_sharink = None
        r_squared = None

# 计算增长率（一阶差分）
growth_rate = np.diff(sharink) / np.diff(counts)

# 创建子图：函数表达式图 + 主图（趋势+拟合）+ 副图（增长率）
# 调整子图顺序，将函数表达式图放在最上面
fig, (ax3, ax1, ax2) = plt.subplots(3, 1, figsize=(16, 16), gridspec_kw={'height_ratios': [1, 6, 3]})

# 新增子图：显示拟合函数表达式和相关性
ax3.axis('off')  # 隐藏坐标轴
if popt is not None and r_squared is not None:
    func_expr = f"拟合函数: f(counts) = {popt[0]:.6f} / (1 + exp(-{popt[2]:.6f} * (counts - {popt[1]:.6f}))) + {popt[3]:.6f}\n相关系数 R$^2$ = {r_squared:.6f}"
    ax3.text(0.5, 0.5, func_expr, transform=ax3.transAxes, fontsize=12, ha='center', va='center',
             bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
else:
    ax3.text(0.5, 0.5, "拟合函数: 无法拟合", transform=ax3.transAxes, fontsize=12, ha='center', va='center',
             bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcoral", alpha=0.7))

# 主图：收缩量随时间变化趋势
ax1.scatter(counts, sharink, s=8, c='#2E86AB', alpha=0.6, label='原始数据', zorder=2)
if fitted_sharink is not None:
    ax1.plot(counts, fitted_sharink, c='#A23B72', linewidth=2.5, label=f'拟合曲线（逻辑增长模型）', zorder=3)

# 标注关键特征点
# 1. 初始点（counts=1）
ax1.scatter(counts[0], sharink[0], c='#F18F01', s=50, marker='*', label='初始点 (1, -1.5e-5)', zorder=5)
ax1.annotate(f'初始点\ncounts=1\nsharink={sharink[0]:.2e}', 
             xy=(counts[0], sharink[0]), xytext=(counts[0]+15, sharink[0]+0.05),
             arrowprops=dict(arrowstyle='->', color='#F18F01', lw=1.5),
             fontsize=10, color='#F18F01', fontweight='bold')

# 2. 快速增长阶段起点（增长率最大值点）
if len(growth_rate) > 0:
    max_growth_idx = np.argmax(growth_rate)
    max_growth_count = counts[:-1][max_growth_idx]
    max_growth_value = growth_rate[max_growth_idx]
    ax1.axvline(x=max_growth_count, c='#C73E1D', linestyle='--', alpha=0.7, label=f'快速增长起点 (counts={max_growth_count:.1f})', zorder=4)
    ax1.annotate(f'快速增长起点\ncounts={max_growth_count:.1f}\n增长率={max_growth_value:.4f}',
                 xy=(max_growth_count, sharink[max_growth_idx]), xytext=(max_growth_count+25, sharink[max_growth_idx]+0.05),
                 arrowprops=dict(arrowstyle='->', color='#C73E1D', lw=1.5),
                 fontsize=10, color='#C73E1D', fontweight='bold')

# 3. 饱和阶段起点（增长率降至最大值的10%）
if len(growth_rate) > 0:
    saturation_threshold = max_growth_value * 0.1
    saturation_indices = np.where(growth_rate < saturation_threshold)[0]
    if len(saturation_indices) > 0:
        saturation_idx = saturation_indices[0]
        saturation_count = counts[:-1][saturation_idx]
        ax1.axvline(x=saturation_count, c='#3F88C5', linestyle='--', alpha=0.7, label=f'饱和阶段起点 (counts={saturation_count:.1f})', zorder=4)
        ax1.annotate(f'饱和阶段起点\ncounts={saturation_count:.1f}\n增长率<{saturation_threshold:.4f}',
                     xy=(saturation_count, sharink[saturation_idx]), xytext=(saturation_count+25, sharink[saturation_idx]-0.05),
                     arrowprops=dict(arrowstyle='->', color='#3F88C5', lw=1.5),
                     fontsize=10, color='#3F88C5', fontweight='bold')

# 主图格式设置
ax1.set_xlabel('时间 (半个月)', fontsize=12, fontweight='bold')
ax1.set_ylabel('收缩量 (sharink)', fontsize=12, fontweight='bold')
ax1.legend(loc='upper left', fontsize=10)
ax1.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
ax1.set_xlim(0, len(shrink_data) + 25)
ax1.set_ylim(min(sharink) - 0.05, max(sharink) + 0.05)

# 副图：增长率变化
if len(growth_rate) > 0:
    ax2.plot(counts[:-1], growth_rate, c='#2E86AB', linewidth=1.5, label='瞬时增长率')
    ax2.axvline(x=max_growth_count, c='#C73E1D', linestyle='--', alpha=0.7, label=f'最大增长率点')
    ax2.axvline(x=saturation_count, c='#3F88C5', linestyle='--', alpha=0.7, label=f'饱和起点')
    ax2.axhline(y=saturation_threshold, c='#888888', linestyle=':', alpha=0.7, label=f'饱和阈值 (10%最大增长率)')

# 副图格式设置
ax2.set_xlabel('时间 (半个月)', fontsize=12, fontweight='bold')
ax2.set_ylabel('(Δsharink/Δcounts)', fontsize=12, fontweight='bold')
ax2.legend(loc='upper right', fontsize=9)
ax2.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
ax2.set_xlim(0, len(shrink_data) + 25)

# 整体布局调整
plt.tight_layout()

# 保存图片（高清格式）
plt.savefig('sharink_change_trend.png', dpi=1200, bbox_inches='tight', facecolor='white')
plt.show()

# 输出关键特征参数
print("=== 收缩量变化规律关键参数 ===")
if popt is not None:
    print(f"拟合模型：sharink = {popt[0]:.4f}/(1 + exp(-{popt[2]:.6f}*(counts-{popt[1]:.4f}))) + {popt[3]:.4f}")
    print(f"最大收缩量（饱和值）：{popt[0] + popt[3]:.4f}")
    # 新增：详细输出拟合函数
    print(f"拟合函数: f(counts) = {popt[0]:.6f} / (1 + exp(-{popt[2]:.6f} * (counts - {popt[1]:.6f}))) + {popt[3]:.6f}")
    if r_squared is not None:
        print(f"拟合相关系数 R^2 = {r_squared:.6f}")
if len(growth_rate) > 0:
    print(f"快速增长起点（最大增长率）：counts={max_growth_count:.1f}, 增长率={max_growth_value:.4f}")
    print(f"饱和阶段起点：counts={saturation_count:.1f}, 对应收缩量={sharink[saturation_idx]:.4f}")
print(f"初始收缩量：{sharink[0]:.6f} (1个半个月)")
print(f"最终收缩量：{sharink[-1]:.4f} ({len(shrink_data)}个半个月)")