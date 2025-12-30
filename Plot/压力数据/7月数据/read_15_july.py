import os
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
import itertools
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
matplotlib.rcParams['axes.unicode_minus'] = False

# 获取当前脚本所在文件夹
folder = os.path.dirname(__file__)

# 查找以15开头的xlsx文件
excel_files = [f for f in os.listdir(folder) if f.endswith('.xlsx') and f.startswith('15')]

# 定义不同的marker样式
markers = ['o', 's', 'D', '^', 'v', '<', '>', 'p', '*', 'h', 'H', 'X', 'd', '|', '_', '+', 'x', '1', '2', '3', '4']
marker_cycle = itertools.cycle(markers)

stat_list = []

for file in excel_files:
    file_path = os.path.join(folder, file)
    df = pd.read_excel(file_path)
    if df.shape[1] < 2:
        print(f"{file} 列数不足2，跳过")
        continue
    # 自动查找时间和数值列
    time_col = [col for col in df.columns[:2] if '时间' in col or 'time' in col.lower()]
    value_col = [col for col in df.columns[:2] if '数值' in col or 'value' in col.lower() or '压力' in col]
    if time_col and value_col:
        try:
            df[time_col[0]] = pd.to_datetime(df[time_col[0]])
        except Exception:
            pass
        # 只保留7月5日以后的数据
        df = df[df[time_col[0]] >= pd.Timestamp('2025-07-05')]
        print(f"{file} 读取成功，数据如下：")
        print(df[[time_col[0], value_col[0]]])
        # 数据分析：找规律、异常、相关性
        if not df.empty:
            print(f"{file} 数据分析：")
            # 1. 描述统计
            desc = df[value_col[0]].describe()
            print("描述统计:")
            print(desc)
            # 2. 异常检测（多种标准）
            mean = desc['mean']
            std = desc['std']
            outliers_3 = df[(df[value_col[0]] > mean + 3*std) | (df[value_col[0]] < mean - 3*std)]
            outliers_2 = df[(df[value_col[0]] > mean + 2*std) | (df[value_col[0]] < mean - 2*std)]
            outliers_1 = df[(df[value_col[0]] > mean + 1*std) | (df[value_col[0]] < mean - 1*std)]
            print(f"异常点数量: 3σ法={len(outliers_3)}, 2σ法={len(outliers_2)}, 1σ法={len(outliers_1)}")
            if not outliers_3.empty:
                print("3σ法异常点:")
                print(outliers_3[[time_col[0], value_col[0]]])
            if not outliers_2.empty:
                print("2σ法异常点:")
                print(outliers_2[[time_col[0], value_col[0]]])
            if not outliers_1.empty:
                print("1σ法异常点:")
                print(outliers_1[[time_col[0], value_col[0]]])
            # 3. 相关性（如有多列可与其他列相关性分析，这里仅一列则略）
            # 4. 简单趋势分析
            if len(df) > 1:
                # 用时间戳与数值做相关性分析
                time_numeric = df[time_col[0]].astype('int64') // 10**9
                corr = df[value_col[0]].corr(time_numeric)
                print(f"数值与时间相关性（趋势性，越接近1越单调）: {corr:.3f}")
            # 保存筛选后的数据
            out_folder = os.path.join(folder, 'output')
            os.makedirs(out_folder, exist_ok=True)
            df_out_path = os.path.join(out_folder, f'{os.path.splitext(file)[0]}_筛选数据.xlsx')
            df[[time_col[0], value_col[0]]].to_excel(df_out_path, index=False)
            print(f"已保存筛选数据: {df_out_path}")
            # 保存异常点数据
            outliers_3_path = os.path.join(out_folder, f'{os.path.splitext(file)[0]}_异常点_3sigma.xlsx')
            outliers_2_path = os.path.join(out_folder, f'{os.path.splitext(file)[0]}_异常点_2sigma.xlsx')
            outliers_1_path = os.path.join(out_folder, f'{os.path.splitext(file)[0]}_异常点_1sigma.xlsx')
            if not outliers_3.empty:
                outliers_3[[time_col[0], value_col[0]]].to_excel(outliers_3_path, index=False)
                print(f"已保存3σ法异常点: {outliers_3_path}")
            if not outliers_2.empty:
                outliers_2[[time_col[0], value_col[0]]].to_excel(outliers_2_path, index=False)
                print(f"已保存2σ法异常点: {outliers_2_path}")
            if not outliers_1.empty:
                outliers_1[[time_col[0], value_col[0]]].to_excel(outliers_1_path, index=False)
                print(f"已保存1σ法异常点: {outliers_1_path}")
            # 新建img5-11文件夹
            img_folder = os.path.join(folder, 'img5-11')
            os.makedirs(img_folder, exist_ok=True)
            # 绘制单表图
            plt.figure(figsize=(12, 6))
            plt.plot(df[time_col[0]], df[value_col[0]], marker='o', linestyle='-', linewidth=1.2, markersize=4, label=file)
            plt.xlabel(time_col[0], fontsize=14)
            plt.ylabel(value_col[0], fontsize=14)
            plt.title(f'{file} 筛选数据变化图', fontsize=16)
            plt.grid(True, linestyle='--', alpha=0.6)
            plt.legend(fontsize=12)
            plt.xticks(rotation=30, fontsize=10)
            plt.yticks(fontsize=10)
            plt.tight_layout()
            img_path = os.path.join(img_folder, f'{os.path.splitext(file)[0]}_筛选数据.png')
            plt.savefig(img_path, dpi=600, bbox_inches='tight', pad_inches=0.2)
            plt.close()
            print(f"已保存筛选数据图像: {img_path}")
    # 汇总数据用于总表
    if 'all_data' not in locals():
        all_data = []
        labels = []
        all_df = []
    all_data.append((df[time_col[0]], df[value_col[0]], os.path.splitext(file)[0]))
    labels.append(os.path.splitext(file)[0])
    # 收集所有筛选数据用于合并输出
    df_tmp = df[[time_col[0], value_col[0]]].copy()
    df_tmp.columns = [f'{os.path.splitext(file)[0]}_时间', f'{os.path.splitext(file)[0]}_数值']
    all_df.append(df_tmp)
    # 汇总统计信息（移到循环内，每个表都append）
    if not df.empty:
        # 汇总统计信息
        stat_info = {
            '文件名': file,
            '数据量': len(df),
            '均值': mean,
            '标准差': std,
            '3σ异常点数': len(outliers_3),
            '2σ异常点数': len(outliers_2),
            '1σ异常点数': len(outliers_1),
            '相关性': corr if len(df) > 1 else None
        }
        stat_list.append(stat_info)
# 汇总总图
if 'all_data' in locals() and all_data:
    plt.figure(figsize=(16, 8))
    for t, v, label in all_data:
        plt.plot(t, v, linewidth=1.2, label=label)
    plt.xlabel('时间', fontsize=14)
    plt.ylabel('数值', fontsize=14)
    plt.title('所有筛选数据总图', fontsize=16)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(fontsize=12)
    plt.xticks(rotation=30, fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout()
    img_path = os.path.join(img_folder, '所有筛选数据总图.png')
    plt.savefig(img_path, dpi=600, bbox_inches='tight', pad_inches=0.2)
    plt.close()
    print(f"已保存所有筛选数据总图: {img_path}")
# 合并所有筛选数据到同一张Excel表
from functools import reduce
df_merged = reduce(lambda left, right: pd.concat([left, right], axis=1), all_df)
excel_path = os.path.join(out_folder, '所有筛选数据合并表.xlsx')
df_merged.to_excel(excel_path, index=False)
print(f"已保存所有筛选数据合并表: {excel_path}")
if stat_list:
    stat_df = pd.DataFrame(stat_list)
    stat_path = os.path.join(out_folder, '所有统计信息汇总.xlsx')
    stat_df.to_excel(stat_path, index=False)
    print(f"已保存所有统计信息汇总表: {stat_path}")
# 汇总总图（异常点标红）
if 'all_data' in locals() and all_data:
    plt.figure(figsize=(16, 8))
    for t, v, label in all_data:
        # 计算均值和标准差
        mean = v.mean()
        std = v.std()
        normal_mask = (v <= mean + 1*std) & (v >= mean - 1*std)
        plt.plot(t[normal_mask], v[normal_mask], linewidth=1.2, label=f'{label} 正常点')
        plt.scatter(t[~normal_mask], v[~normal_mask], color='red', marker='o', s=30, label=f'{label} 异常点(>1σ)')
    plt.xlabel('时间', fontsize=14)
    plt.ylabel('数值', fontsize=14)
    plt.title('所有筛选数据总图(异常点标红)', fontsize=16)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(fontsize=12)
    plt.xticks(rotation=30, fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout()
    img_path = os.path.join(img_folder, '所有筛选数据总图_异常点标红.png')
    plt.savefig(img_path, dpi=600, bbox_inches='tight', pad_inches=0.2)
    plt.close()
    print(f"已保存所有筛选数据总图(异常点标红): {img_path}")
