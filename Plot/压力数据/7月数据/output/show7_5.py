import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
matplotlib.rcParams['axes.unicode_minus'] = False

folder = os.path.dirname(__file__)
img_folder = os.path.join(folder, 'img7_5')
os.makedirs(img_folder, exist_ok=True)

excel_files = [f for f in os.listdir(folder) if f.endswith('筛选数据.xlsx')]
all_data = []
labels = []

for file in excel_files:
    file_path = os.path.join(folder, file)
    try:
        df = pd.read_excel(file_path)
        # 自动查找时间和数值列
        time_col = [col for col in df.columns if '时间' in col or 'time' in col.lower()]
        value_col = [col for col in df.columns if '数值' in col or 'value' in col.lower() or '压力' in col]
        if time_col and value_col:
            df[time_col[0]] = pd.to_datetime(df[time_col[0]])
            # 筛选7月5日2点到3点的数据
            mask = (df[time_col[0]] >= pd.Timestamp('2025-07-05 02:00:00')) & (df[time_col[0]] <= pd.Timestamp('2025-07-05 03:00:00'))
            df_sel = df[mask]
            if not df_sel.empty:
                # 绘制单表图
                plt.figure(figsize=(12, 6))
                plt.plot(df_sel[time_col[0]], df_sel[value_col[0]], marker='o', linestyle='-', linewidth=1.2, markersize=4, label=file)
                plt.xlabel(time_col[0], fontsize=14)
                plt.ylabel(value_col[0], fontsize=14)
                plt.title(f'{file} 7月5日2-3点数据曲线', fontsize=16)
                plt.grid(True, linestyle='--', alpha=0.6)
                plt.legend(fontsize=12)
                plt.xticks(rotation=30, fontsize=10)
                plt.yticks(fontsize=10)
                plt.tight_layout()
                img_path = os.path.join(img_folder, f'{os.path.splitext(file)[0]}_7月5日2-3点.png')
                plt.savefig(img_path, dpi=600, bbox_inches='tight', pad_inches=0.2)
                plt.close()
                print(f"已保存单表图像: {img_path}")
                # 收集数据用于总图
                all_data.append((df_sel[time_col[0]], df_sel[value_col[0]], os.path.splitext(file)[0]))
                labels.append(os.path.splitext(file)[0])
    except Exception as e:
        print(f'读取 {file} 时出错: {e}')

# 绘制总图
if all_data:
    plt.figure(figsize=(16, 8))
    for t, v, label in all_data:
        plt.plot(t, v, linewidth=1.2, label=label)
    plt.xlabel('时间', fontsize=14)
    plt.ylabel('数值', fontsize=14)
    plt.title('所有文件 7月5日2-3点数据总图', fontsize=16)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(fontsize=12)
    plt.xticks(rotation=30, fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout()
    img_path = os.path.join(img_folder, '所有文件_7月5日2-3点总图.png')
    plt.savefig(img_path, dpi=600, bbox_inches='tight', pad_inches=0.2)
    plt.close()
    print(f"已保存所有文件总图: {img_path}")
else:
    print('没有筛选出 7月5日2-3点 的数据。')
