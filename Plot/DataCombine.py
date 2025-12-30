import os
import pandas as pd

# 路径设置
base_folder = os.path.dirname(__file__)
src_folder = os.path.join(base_folder, '压力数据')
folder_6 = os.path.join(src_folder, '6月数据')
folder_7 = os.path.join(src_folder, '7月数据')
out_folder = os.path.join(src_folder, '6-7月数据')
os.makedirs(out_folder, exist_ok=True)

# 获取两个文件夹下的所有Excel文件名
files_6 = set([f for f in os.listdir(folder_6) if f.endswith('.xlsx')])
files_7 = set([f for f in os.listdir(folder_7) if f.endswith('.xlsx')])

# 找到两个文件夹中都存在的文件
common_files = files_6 & files_7


# 合并所有表到一个总表（不对齐时间，直接拼接，表头重命名）
merged_dfs = []
for fname in common_files:
    out_path = os.path.join(out_folder, fname)
    path_6 = os.path.join(folder_6, fname)
    path_7 = os.path.join(folder_7, fname)
    df6 = pd.read_excel(path_6)
    df7 = pd.read_excel(path_7)
    # 拼接，6月在前，7月在后
    df_all = pd.concat([df6, df7], ignore_index=True)
    df_all.to_excel(out_path, index=False)
    print(f"已合并并保存: {out_path}")
    # 只读取前两列，并重命名为“文件名+原表头”
    if df_all.shape[1] >= 2:
        col1, col2 = df_all.columns[:2]
        new_col1 = os.path.splitext(fname)[0] + str(col1)
        new_col2 = os.path.splitext(fname)[0] + str(col2)
        df_tmp = df_all.iloc[:, :2].copy()
        df_tmp.columns = [new_col1, new_col2]
        merged_dfs.append(df_tmp)

# 拼接所有表（不对齐，直接竖向拼接）
if merged_dfs:
    df_merged = pd.concat(merged_dfs, axis=0, ignore_index=True)
    out_path = os.path.join(out_folder, '6-7月所有表拼接数据.xlsx')
    df_merged.to_excel(out_path, index=False)
    print(f"所有表已拼接并保存: {out_path}")
