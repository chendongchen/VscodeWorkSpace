import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
from mpl_toolkits.mplot3d import Axes3D

# 设置matplotlib支持中文
rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
rcParams['axes.unicode_minus'] = False

# 获取当前脚本所在文件夹
folder = os.path.dirname(__file__)


# 创建img文件夹
img_folder = os.path.join(folder, 'img')
os.makedirs(img_folder, exist_ok=True)

# 查找所有xlsx文件
excel_files = [f for f in os.listdir(folder) if f.endswith('.xlsx')]



# 单表二维绘图
all_data = []
labels = []
for file in excel_files:
    file_path = os.path.join(folder, file)
    df = pd.read_excel(file_path)
    time_col = [col for col in df.columns if '时间' in col or 'time' in col.lower()]
    value_col = [col for col in df.columns if '数值' in col or 'value' in col.lower()]
    if time_col and value_col:
        df[time_col[0]] = pd.to_datetime(df[time_col[0]])
        # 保存单表二维图
        plt.figure(figsize=(12, 6))
        plt.plot(df[time_col[0]], df[value_col[0]], linestyle='-', linewidth=2, label=os.path.splitext(file)[0])
        plt.xlabel(time_col[0], fontsize=14)
        plt.ylabel('压力（mPa）', fontsize=14)
        plt.title(f'{os.path.splitext(file)[0]} 压力随时间变化曲线', fontsize=16)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend(fontsize=12)
        plt.xticks(rotation=30, fontsize=10)
        plt.yticks(fontsize=10)
        plt.tight_layout()
        img_path = os.path.join(img_folder, f'{os.path.splitext(file)[0]}_2d.png')
        plt.savefig(img_path, dpi=400, bbox_inches='tight', pad_inches=0.2)
        plt.close()
        print(f"已保存单表二维图片: {img_path}")
        # 收集数据用于合并绘图
        all_data.append((df[time_col[0]], df[value_col[0]], os.path.splitext(file)[0]))
        labels.append(os.path.splitext(file)[0])
    else:
        print(f"{file} 未找到合适的时间或数值列")

# 合并二维绘图
if all_data:
    plt.figure(figsize=(16, 8))
    for t, v, label in all_data:
        plt.plot(t, v, linewidth=2, label=label)
    plt.xlabel('时间', fontsize=14)
    plt.ylabel('压力（mPa）', fontsize=14)
    plt.title('所有表压力随时间变化曲线', fontsize=16)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(fontsize=12)
    plt.xticks(rotation=30, fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout()
    img_path = os.path.join(img_folder, '所有表压力曲线_2d.png')
    plt.savefig(img_path, dpi=400, bbox_inches='tight', pad_inches=0.2)
    plt.close()
    print(f"已保存所有表二维图片: {img_path}")

# 合并三维绘图
if all_data:
    from mpl_toolkits.mplot3d import Axes3D
    import datetime
    fig = plt.figure(figsize=(20, 12))
    ax = fig.add_subplot(111, projection='3d')
    for idx, (t, v, label) in enumerate(all_data):
        t_num = t.map(lambda x: x.timestamp())
        z = [idx] * len(t)
        ax.plot(t_num, z, v, label=label, linewidth=2)
    ax.set_xlabel('时间', fontsize=14)
    ax.set_ylabel('文件', fontsize=14)
    ax.set_zlabel('压力（mPa）', fontsize=14)
    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels, fontsize=12)
    def format_time(x, pos=None):
        return datetime.datetime.fromtimestamp(x).strftime('%Y-%m-%d\n%H:%M')
    ax.xaxis.set_major_formatter(plt.FuncFormatter(format_time))
    plt.title('所有表压力随时间变化三维曲线', fontsize=18)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(fontsize=12)
    img_path = os.path.join(img_folder, '所有表压力曲线_3d.png')
    plt.savefig(img_path, dpi=400, bbox_inches='tight', pad_inches=0.2)
    plt.close()
    print(f"已保存所有表三维图片: {img_path}")