import numpy as np
import matplotlib.pyplot as plt

print('hello')

# 生成随机数组
random_data = np.random.normal(loc=0, scale=1, size=1000)
short_random_data = random_data
print(short_random_data)

# 生成 x 轴数据
x_line = [1] * 1000
print(x_line)

# 排序随机数据
sorted_data = np.sort(short_random_data)
print(sorted_data)

# 创建图表
plt.figure(figsize=(12, 6))

# 子图 1: 原始数据直方图
plt.subplot(1, 2, 1)
plt.bar(random_data, x_line, width=0.005, color='blue')
plt.title('Original Data')
plt.xlabel('Value')
plt.ylabel('Frequency')

# 子图 2: 排序后数据直方图
plt.subplot(1, 2, 2)
plt.bar(sorted_data, x_line, width=0.005, color='blue')
plt.title('Sorted Data')
plt.xlabel('Value')
plt.ylabel('Frequency')

plt.tight_layout()
plt.show()