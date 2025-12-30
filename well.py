import matplotlib.pyplot as plt

# 坐标点数据
points = {
    'HJ09': (494625.63, 3988794.01),
    'HJ10': (494622.6, 3989065.8),
    'HJ11': (494831.91, 3988935.65),
    'HJ12': (494831.15, 3989224.6),
    'HJ13': (495033.65, 3988942.2),
    'HJ14': (495022.89, 3989224.95),
    'HJ15': (495224.83, 3988928.35),
    'HJ16': (495227.53, 3989211.77),
    'HJ17': (495427.21, 3988921.38),
    'HJ18': (495427.55, 3989205),
    'HJ05': (495226.58, 3988553.05),
    'HJ06': (495227.7, 3988832.8),
    'HJ03': (495023.09, 3988572.45),
    'HJ04': (495035.47, 3988828.67),
    'HJ01': (494824.45, 3988544.55),
    'HJ02': (494824.3, 3988832.96)
}

# 提取x和y坐标
x_coords = [coord[0] for coord in points.values()]
y_coords = [coord[1] for coord in points.values()]

# 创建图形
plt.figure(figsize=(10, 8))
plt.scatter(x_coords, y_coords, c='red', s=50)

# 添加标签
for label, (x, y) in points.items():
    plt.annotate(label, (x, y), xytext=(5, 5), textcoords='offset points', fontsize=9)

# 设置图形属性
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.title('Coordinate Points Distribution')
plt.grid(True, alpha=0.3)

# 调整坐标轴以更好地显示点位
plt.tight_layout()

# 显示图形
plt.show()