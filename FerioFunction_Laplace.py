import sympy as sp
import numpy as np
import matplotlib
matplotlib.use('TkAgg')  # 设置后端
import matplotlib.pyplot as plt

# 定义符号变量
t, w = sp.symbols('t w')
T = 1.0  # 周期
h = 1.0  # 高度

# 定义锯齿波函数
sawtooth_wave = h * (t % T) / T

# 手动计算傅里叶变换
# 锯齿波的傅里叶变换结果
fourier_transform = h * (1 - sp.exp(-sp.I * w * T)) / (sp.I * w * T)

# 将符号表达式转换为数值函数
fourier_transform_func = sp.lambdify(w, fourier_transform, 'numpy')

# 生成频率向量
w_values = np.linspace(-10, 10, 1000)

# 计算频谱值
spectrum_values = fourier_transform_func(w_values)

# 绘制频谱图
plt.figure(figsize=(12, 6))

# 双边幅度频谱
plt.subplot(2, 1, 1)
plt.plot(w_values, np.abs(spectrum_values))
plt.title('Double-Sided Amplitude Spectrum')
plt.xlabel('Frequency (w)')
plt.ylabel('Magnitude')

# 单边幅度频谱
positive_w_values = w_values[w_values >= 0]
positive_spectrum_values = spectrum_values[w_values >= 0]

plt.subplot(2, 1, 2)
plt.plot(positive_w_values, np.abs(positive_spectrum_values))
plt.title('Single-Sided Amplitude Spectrum')
plt.xlabel('Frequency (w)')
plt.ylabel('Magnitude')

plt.tight_layout()
plt.show()