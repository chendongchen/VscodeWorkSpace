import os
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import matplotlib

# 获取当前脚本所在文件夹
folder = os.path.dirname(__file__)

# 查找以“筛选数据”结尾的xlsx文件
excel_files = [f for f in os.listdir(folder) if f.endswith('筛选数据.xlsx')]

results = []
if not excel_files:
    print('未找到以“筛选数据”结尾的Excel文件。')
else:
    matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
    matplotlib.rcParams['axes.unicode_minus'] = False

    out_dir = os.path.join(folder, 'analysisout')
    os.makedirs(out_dir, exist_ok=True)

    for file in excel_files:
        file_path = os.path.join(folder, file)
        try:
            df = pd.read_excel(file_path)
            # 自动查找时间和数值列
            time_col = [col for col in df.columns if '时间' in col or 'time' in col.lower()]
            value_col = [col for col in df.columns if '数值' in col or 'value' in col.lower() or '压力' in col]
            if time_col and value_col:
                try:
                    df[time_col[0]] = pd.to_datetime(df[time_col[0]])
                    time_numeric = df[time_col[0]].astype('int64') // 10**9
                    X = time_numeric.values.reshape(-1, 1)
                    y = df[value_col[0]].values
                    # 分割点：7月8日
                    split_time = pd.Timestamp('2025-07-08')
                    mask1 = df[time_col[0]] < split_time
                    mask2 = df[time_col[0]] >= split_time
                    # 第一段
                    X1 = time_numeric[mask1].values.reshape(-1, 1)
                    y1 = df.loc[mask1, value_col[0]].values
                    # 第二段
                    X2 = time_numeric[mask2].values.reshape(-1, 1)
                    y2 = df.loc[mask2, value_col[0]].values
                    # 回归
                    model1 = LinearRegression()
                    model2 = LinearRegression()
                    # 普通线性回归
                    model_all = LinearRegression()
                    if len(X) > 1:
                        model_all.fit(X, y)
                        slope_all = model_all.coef_[0] * 86400
                        intercept_all = model_all.intercept_
                        score_all = model_all.score(X, y)
                        # 普通回归线
                        y_all_pred = model_all.predict(X)
                        plt.plot(df[time_col[0]], y_all_pred, color='orange', linewidth=2, label='普通回归')
                        formula_all = f'普通: y = {slope_all:.4f} * 天 + {intercept_all:.2f}\n$R^2$ = {score_all:.4f}'
                        plt.text(0.05, 0.70, formula_all, transform=plt.gca().transAxes, fontsize=12, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.7))
                    else:
                        slope_all = intercept_all = score_all = None
                    if len(X1) > 1:
                        model1.fit(X1, y1)
                        slope1 = model1.coef_[0] * 86400
                        intercept1 = model1.intercept_
                        score1 = model1.score(X1, y1)
                        y1_pred = model1.predict(X1)
                    else:
                        slope1 = intercept1 = score1 = y1_pred = None
                    if len(X2) > 1:
                        model2.fit(X2, y2)
                        slope2 = model2.coef_[0] * 86400
                        intercept2 = model2.intercept_
                        score2 = model2.score(X2, y2)
                        y2_pred = model2.predict(X2)
                    else:
                        slope2 = intercept2 = score2 = y2_pred = None
                    # 自动寻找最优分割点（最小总RSS）
                    best_rss = float('inf')
                    best_idx = None
                    best_results = None
                    n = len(df)
                    min_points = max(2, int(0.1 * n))  # 两端至少保留2个点或10%
                    for split in range(min_points, n - min_points):
                        mask1 = df.index < split
                        mask2 = df.index >= split
                        if mask1.sum() < 2 or mask2.sum() < 2:
                            continue
                        X1 = time_numeric[mask1].values.reshape(-1, 1)
                        y1 = df.loc[mask1, value_col[0]].values
                        X2 = time_numeric[mask2].values.reshape(-1, 1)
                        y2 = df.loc[mask2, value_col[0]].values
                        m1 = LinearRegression()
                        m2 = LinearRegression()
                        m1.fit(X1, y1)
                        m2.fit(X2, y2)
                        rss1 = ((y1 - m1.predict(X1)) ** 2).sum()
                        rss2 = ((y2 - m2.predict(X2)) ** 2).sum()
                        total_rss = rss1 + rss2
                        if total_rss < best_rss:
                            best_rss = total_rss
                            best_idx = split
                            best_results = {
                                'slope1': m1.coef_[0] * 86400,
                                'intercept1': m1.intercept_,
                                'score1': m1.score(X1, y1),
                                'y1_pred': m1.predict(X1),
                                'mask1': mask1,
                                'slope2': m2.coef_[0] * 86400,
                                'intercept2': m2.intercept_,
                                'score2': m2.score(X2, y2),
                                'y2_pred': m2.predict(X2),
                                'mask2': mask2,
                                'split_time': df.loc[split, time_col[0]]
                            }
                    # 自动寻找最优2段分割点（最小总RSS）
                    best_rss = float('inf')
                    best_idx = None
                    best_results = None
                    n = len(df)
                    min_points = max(2, int(0.1 * n))  # 两端至少保留2个点或10%
                    for split in range(min_points, n - min_points):
                        mask1 = df.index < split
                        mask2 = df.index >= split
                        if mask1.sum() < 2 or mask2.sum() < 2:
                            continue
                        X1 = time_numeric[mask1].values.reshape(-1, 1)
                        y1 = df.loc[mask1, value_col[0]].values
                        X2 = time_numeric[mask2].values.reshape(-1, 1)
                        y2 = df.loc[mask2, value_col[0]].values
                        m1 = LinearRegression()
                        m2 = LinearRegression()
                        m1.fit(X1, y1)
                        m2.fit(X2, y2)
                        rss1 = ((y1 - m1.predict(X1)) ** 2).sum()
                        rss2 = ((y2 - m2.predict(X2)) ** 2).sum()
                        total_rss = rss1 + rss2
                        if total_rss < best_rss:
                            best_rss = total_rss
                            best_idx = split
                            best_results = {
                                'slope1': m1.coef_[0] * 86400,
                                'intercept1': m1.intercept_,
                                'score1': m1.score(X1, y1),
                                'y1_pred': m1.predict(X1),
                                'mask1': mask1,
                                'slope2': m2.coef_[0] * 86400,
                                'intercept2': m2.intercept_,
                                'score2': m2.score(X2, y2),
                                'y2_pred': m2.predict(X2),
                                'mask2': mask2,
                                'split_time': df.loc[split, time_col[0]]
                            }
                    # 自动寻找最优3段分割点（最小总RSS），以2段分割点附近为中心
                    best_rss3 = float('inf')
                    best_idx1 = None
                    best_idx2 = None
                    best_results3 = None
                    search_range = 10 if best_idx else 0
                    for split1 in range(max(min_points, (best_idx or min_points) - search_range), min(n - min_points*2, (best_idx or min_points) + search_range)):
                        for split2 in range(split1 + min_points, n - min_points):
                            mask1 = df.index < split1
                            mask2 = (df.index >= split1) & (df.index < split2)
                            mask3 = df.index >= split2
                            if mask1.sum() < 2 or mask2.sum() < 2 or mask3.sum() < 2:
                                continue
                            X1 = time_numeric[mask1].values.reshape(-1, 1)
                            y1 = df.loc[mask1, value_col[0]].values
                            X2 = time_numeric[mask2].values.reshape(-1, 1)
                            y2 = df.loc[mask2, value_col[0]].values
                            X3 = time_numeric[mask3].values.reshape(-1, 1)
                            y3 = df.loc[mask3, value_col[0]].values
                            m1 = LinearRegression()
                            m2 = LinearRegression()
                            m3 = LinearRegression()
                            m1.fit(X1, y1)
                            m2.fit(X2, y2)
                            m3.fit(X3, y3)
                            rss1 = ((y1 - m1.predict(X1)) ** 2).sum()
                            rss2 = ((y2 - m2.predict(X2)) ** 2).sum()
                            rss3 = ((y3 - m3.predict(X3)) ** 2).sum()
                            total_rss3 = rss1 + rss2 + rss3
                            if total_rss3 < best_rss3:
                                best_rss3 = total_rss3
                                best_idx1 = split1
                                best_idx2 = split2
                                best_results3 = {
                                    'slope1': m1.coef_[0] * 86400,
                                    'intercept1': m1.intercept_,
                                    'score1': m1.score(X1, y1),
                                    'y1_pred': m1.predict(X1),
                                    'mask1': mask1,
                                    'slope2': m2.coef_[0] * 86400,
                                    'intercept2': m2.intercept_,
                                    'score2': m2.score(X2, y2),
                                    'y2_pred': m2.predict(X2),
                                    'mask2': mask2,
                                    'slope3': m3.coef_[0] * 86400,
                                    'intercept3': m3.intercept_,
                                    'score3': m3.score(X3, y3),
                                    'y3_pred': m3.predict(X3),
                                    'mask3': mask3,
                                    'split_time1': df.loc[split1, time_col[0]],
                                    'split_time2': df.loc[split2, time_col[0]]
                                }
                    # 用最优分割点结果替换原分段回归
                    if best_results:
                        slope1 = best_results['slope1']
                        intercept1 = best_results['intercept1']
                        score1 = best_results['score1']
                        y1_pred = best_results['y1_pred']
                        mask1 = best_results['mask1']
                        slope2 = best_results['slope2']
                        intercept2 = best_results['intercept2']
                        score2 = best_results['score2']
                        y2_pred = best_results['y2_pred']
                        mask2 = best_results['mask2']
                        split_time = best_results['split_time']
                    # 3段分割结果
                    if best_results3:
                        slope3_1 = best_results3['slope1']
                        intercept3_1 = best_results3['intercept1']
                        score3_1 = best_results3['score1']
                        y3_1_pred = best_results3['y1_pred']
                        mask3_1 = best_results3['mask1']
                        slope3_2 = best_results3['slope2']
                        intercept3_2 = best_results3['intercept2']
                        score3_2 = best_results3['score2']
                        y3_2_pred = best_results3['y2_pred']
                        mask3_2 = best_results3['mask2']
                        slope3_3 = best_results3['slope3']
                        intercept3_3 = best_results3['intercept3']
                        score3_3 = best_results3['score3']
                        y3_3_pred = best_results3['y3_pred']
                        mask3_3 = best_results3['mask3']
                        split_time1 = best_results3['split_time1']
                        split_time2 = best_results3['split_time2']
                    else:
                        slope3_1 = intercept3_1 = score3_1 = y3_1_pred = mask3_1 = None
                        slope3_2 = intercept3_2 = score3_2 = y3_2_pred = mask3_2 = None
                        slope3_3 = intercept3_3 = score3_3 = y3_3_pred = mask3_3 = None
                        split_time1 = split_time2 = None
                    # 结果只append一次，包含所有回归结果
                    results.append({
                        '文件': file,
                        '普通_斜率(每天)': slope_all if len(X) > 1 else None,
                        '普通_截距': intercept_all if len(X) > 1 else None,
                        '普通_R^2': score_all if len(X) > 1 else None,
                        '分段1_斜率(每天)': slope1,
                        '分段1_截距': intercept1,
                        '分段1_R^2': score1,
                        '分段2_斜率(每天)': slope2,
                        '分段2_截距': intercept2,
                        '分段2_R^2': score2,
                        '分段点': str(split_time),
                        '三段1_斜率(每天)': slope3_1,
                        '三段1_截距': intercept3_1,
                        '三段1_R^2': score3_1,
                        '三段2_斜率(每天)': slope3_2,
                        '三段2_截距': intercept3_2,
                        '三段2_R^2': score3_2,
                        '三段3_斜率(每天)': slope3_3,
                        '三段3_截距': intercept3_3,
                        '三段3_R^2': score3_3,
                        '三段分割点1': str(split_time1),
                        '三段分割点2': str(split_time2)
                    })
                    # 绘图（同一表所有分段回归线和原始数据在同一图中）
                    plt.figure(figsize=(12, 6))
                    plt.scatter(df[time_col[0]], y, color='blue', s=20, label='原始数据')
                    # 普通回归线（用全局时间范围绘制，确保为直线）
                    if len(X) > 1:
                        t_min = df[time_col[0]].min()
                        t_max = df[time_col[0]].max()
                        t_line = pd.date_range(start=t_min, end=t_max, periods=100)
                        t_line_numeric = t_line.astype('int64') // 10**9
                        y_line = model_all.predict(t_line_numeric.values.reshape(-1, 1))
                        plt.plot(t_line, y_line, color='orange', linewidth=2, label='普通回归')
                        formula_all = f'普通: y = {slope_all:.4f} * 天 + {intercept_all:.2f}\n$R^2$ = {score_all:.4f}'
                        plt.text(0.05, 0.70, formula_all, transform=plt.gca().transAxes, fontsize=12, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.7))
                    # 2段回归线
                    if len(X1) > 1:
                        plt.plot(df.loc[mask1, time_col[0]], y1_pred, color='red', linewidth=2, label='分段1回归')
                        formula1 = f'段1: y = {slope1:.4f} * 天 + {intercept1:.2f}\n$R^2$ = {score1:.4f}'
                        plt.text(0.05, 0.90, formula1, transform=plt.gca().transAxes, fontsize=12, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.7))
                    if len(X2) > 1:
                        plt.plot(df.loc[mask2, time_col[0]], y2_pred, color='green', linewidth=2, label='分段2回归')
                        formula2 = f'段2: y = {slope2:.4f} * 天 + {intercept2:.2f}\n$R^2$ = {score2:.4f}'
                        plt.text(0.05, 0.80, formula2, transform=plt.gca().transAxes, fontsize=12, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.7))
                    # 2段分割点
                    if best_results:
                        plt.axvline(split_time, color='purple', linestyle='--', linewidth=2, label='最优2段分割点')
                    # 3段回归线
                    if best_results3:
                        if mask3_1 is not None:
                            plt.plot(df.loc[mask3_1, time_col[0]], y3_1_pred, color='brown', linewidth=2, label='三段1回归')
                            formula3_1 = f'三段1: y = {slope3_1:.4f} * 天 + {intercept3_1:.2f}\n$R^2$ = {score3_1:.4f}'
                            plt.text(0.05, 0.60, formula3_1, transform=plt.gca().transAxes, fontsize=12, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.7))
                        if mask3_2 is not None:
                            plt.plot(df.loc[mask3_2, time_col[0]], y3_2_pred, color='magenta', linewidth=2, label='三段2回归')
                            formula3_2 = f'三段2: y = {slope3_2:.4f} * 天 + {intercept3_2:.2f}\n$R^2$ = {score3_2:.4f}'
                            plt.text(0.05, 0.50, formula3_2, transform=plt.gca().transAxes, fontsize=12, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.7))
                        if mask3_3 is not None:
                            plt.plot(df.loc[mask3_3, time_col[0]], y3_3_pred, color='cyan', linewidth=2, label='三段3回归')
                            formula3_3 = f'三段3: y = {slope3_3:.4f} * 天 + {intercept3_3:.2f}\n$R^2$ = {score3_3:.4f}'
                            plt.text(0.05, 0.40, formula3_3, transform=plt.gca().transAxes, fontsize=12, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.7))
                        # 3段分割点
                        if split_time1 is not None:
                            plt.axvline(split_time1, color='black', linestyle='--', linewidth=2, label='三段分割点1')
                        if split_time2 is not None:
                            plt.axvline(split_time2, color='gray', linestyle='--', linewidth=2, label='三段分割点2')
                    plt.title(f'{file} 分段线性回归分析', fontsize=16)
                    plt.xlabel(time_col[0], fontsize=14)
                    plt.ylabel(value_col[0], fontsize=14)
                    plt.legend(fontsize=12)
                    plt.grid(True, linestyle='--', alpha=0.6)
                    plt.xticks(rotation=30, fontsize=10)
                    plt.yticks(fontsize=10)
                    plt.tight_layout()
                    img_path = os.path.join(out_dir, f'{os.path.splitext(file)[0]}_分段回归分析图.png')
                    plt.savefig(img_path, dpi=600, bbox_inches='tight', pad_inches=0.2)
                    plt.close()
                except Exception as e:
                    results.append({
                        '文件': file,
                        '分段1_斜率(每天)': None,
                        '分段1_截距': None,
                        '分段1_R^2': None,
                        '分段2_斜率(每天)': None,
                        '分段2_截距': None,
                        '分段2_R^2': None,
                        '错误': str(e)
                    })
        except Exception as e:
            results.append({
                '文件': file,
                '分段1_斜率(每天)': None,
                '分段1_截距': None,
                '分段1_R^2': None,
                '分段2_斜率(每天)': None,
                '分段2_截距': None,
                '分段2_R^2': None,
                '错误': str(e)
            })
if results:
    df_result = pd.DataFrame(results)
    out_path = os.path.join(out_dir, '分段线性回归分析结果.xlsx')
    df_result.to_excel(out_path, index=False)
    print(f'已保存分段分析结果: {out_path}')

