import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
import itertools

# 设置matplotlib支持中文
rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
rcParams['axes.unicode_minus'] = False

# 获取当前脚本所在文件夹
folder = os.path.dirname(__file__)

# 创建img文件夹
img_folder = os.path.join(folder, 'img')
os.makedirs(img_folder, exist_ok=True)

# 查找所有xlsx文件（排除合并总表）
excel_files = [f for f in os.listdir(folder) if f.endswith('.xlsx') and '合并' not in f and '拼接' not in f]

# 定义不同的marker样式
markers = ['o', 's', 'D', '^', 'v', '<', '>', 'p', '*', 'h', 'H', 'X', 'd', '|', '_', '+', 'x', '1', '2', '3', '4']
marker_cycle = itertools.cycle(markers)

for file in excel_files:
    file_path = os.path.join(folder, file)
    df = pd.read_excel(file_path)
    # 自动查找时间和数值列
    time_col = [col for col in df.columns if '时间' in col or 'time' in col.lower()]
    value_col = [col for col in df.columns if '数值' in col or 'value' in col.lower() or '压力' in col]
    if time_col and value_col:
        try:
            df[time_col[0]] = pd.to_datetime(df[time_col[0]])
        except Exception:
            pass
        marker = next(marker_cycle)
        plt.figure(figsize=(14, 7))
        plt.plot(df[time_col[0]], df[value_col[0]], marker=marker, linestyle='-', linewidth=1.2, markersize=4, label=file)
        plt.xlabel(time_col[0], fontsize=14)
        plt.ylabel(value_col[0], fontsize=14)
        plt.title(f'{file} 数据变化点线图', fontsize=16)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend(fontsize=12)
        plt.xticks(rotation=30, fontsize=10)
        plt.yticks(fontsize=10)
        plt.tight_layout()
        img_path = os.path.join(img_folder, f'{os.path.splitext(file)[0]}_2d.png')
        plt.savefig(img_path, dpi=600, bbox_inches='tight', pad_inches=0.2)
        plt.close()
        print(f"已保存图片: {img_path}")
    else:
        print(f"{file} 未找到合适的时间或数值列")

# 汇总所有表的曲线到一张图
all_data = []
labels = []
marker_cycle = itertools.cycle(markers)
for file in excel_files:
    file_path = os.path.join(folder, file)
    df = pd.read_excel(file_path)
    time_col = [col for col in df.columns if '时间' in col or 'time' in col.lower()]
    value_col = [col for col in df.columns if '数值' in col or 'value' in col.lower() or '压力' in col]
    if time_col and value_col:
        try:
            df[time_col[0]] = pd.to_datetime(df[time_col[0]])
        except Exception:
            pass
        all_data.append((df[time_col[0]], df[value_col[0]], os.path.splitext(file)[0], next(marker_cycle)))
        labels.append(os.path.splitext(file)[0])

if all_data:
    plt.figure(figsize=(18, 9))
    for t, v, label, marker in all_data:
        plt.plot(t, v, marker=marker, linewidth=1.2, markersize=4, label=label)
    plt.xlabel('时间', fontsize=14)
    plt.ylabel('压力', fontsize=14)
    plt.title('所有表数据变化汇总图', fontsize=16)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(fontsize=12)
    plt.xticks(rotation=30, fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout()
    img_path = os.path.join(img_folder, '所有表数据变化汇总图.png')
    plt.savefig(img_path, dpi=600, bbox_inches='tight', pad_inches=0.2)
    plt.close()
    print(f"已保存所有表汇总图片: {img_path}")
