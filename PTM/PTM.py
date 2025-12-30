import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
from scipy.stats import chi2_contingency
from sklearn.metrics import pairwise_distances

matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 支持中文字体显示
matplotlib.rcParams['axes.unicode_minus'] = False

# 1. 读取数据
# 注意文件路径
# 建议先输出所有列名，便于后续核对

df = pd.read_excel('PTM/statics.xlsx')
# print('实际表头列名如下：')
# print(list(df.columns))

# 2. 选择分组变量和协变量
group_col = '学业压力总分'  # 例如：高学业压力（1）vs低学业压力（0），请根据实际列名修改
covariates = ['2、你的年龄:  ', '3、你的年级:  ', '4、你的性别:  ', '你的民族  ',
               '7、你的专业:  ', '8、你的家庭所在地:  ', '9、你是否为独生子女:  ', 
               '10、父母对你的态度:  ', '11、你的家庭状况如何:  ', '12、留守经历', 
               '13、你的运动频率（每周≥3次，≥30min/次）:  ', '14、你的睡眠情况:  ', '15、你每天看多久手机:  ', 
                '学业前景压力总', '学业竞争压力总', '学习成效压力总', '学习气氛压力总', '课业负担压力总', '学习条件压力总', 
                '家庭期望压力总', '学习能力自我效能感', '学习行为自我效能感',  
                '负面评价恐惧总分', '积极应对方式总分', '消极应对方式总分', '抑郁总分', '焦虑总分', '压力总分',  '家庭关怀总分', '智慧型幸福总分'
               ]  # 替换为实际协变量

# covariates前半部分用于模式匹配，后半部分用于网络分析
split_idx = 13  # 假设前13个协变量用于匹配，后面的用于网络分析
# print(covariates[13])
covariates_match = covariates[:split_idx]
covariates_network = covariates[split_idx:]
# print(f'协变量匹配部分：{covariates_match}')
# print(f'协变量网络分析部分：{covariates_network}')
# 2.5 对协变量做独热编码，保证全部为数值型
# 先去除group_col和covariates_match中有缺失值的行
use_cols = [group_col] + covariates_match
data = df[use_cols].dropna()
X = pd.get_dummies(data[covariates_match], drop_first=True).fillna(0)
y = data[group_col]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 3. 计算倾向得分
model = LogisticRegression(max_iter=5000)
model.fit(X_scaled, y)
data['propensity_score'] = model.predict_proba(X_scaled)[:, 1]

# 以中位数为阈值，分为高低压力组
threshold = data[group_col].median()
data['group'] = (data[group_col] >= threshold).astype(int)

# 4. 进行1:1最近邻匹配
# 后续全部用data而不是df

# 匹配分组
treated = data[data['group'] == 1]
control = data[data['group'] == 0]
nn = NearestNeighbors(n_neighbors=1)
nn.fit(control[['propensity_score']])
distances, indices = nn.kneighbors(treated[['propensity_score']])
matched_control = control.iloc[indices.flatten()]
matched_df = pd.concat([treated, matched_control])

# 输出匹配结果到Excel
matched_df.to_excel('PTM/matched_result.xlsx', index=False)

# 统计匹配前后高低压力组各标签的频数和百分比，并做卡方检验（仅对匹配用的变量）
stat_result = []
def count_percent(series):
    return series.value_counts().to_dict(), (series.value_counts(normalize=True)*100).round(2).to_dict()

for col in covariates_match:
    # 匹配前统计
    pre_high_count, pre_high_pct = count_percent(data[data['group']==1][col])
    pre_low_count, pre_low_pct = count_percent(data[data['group']==0][col])
    try:
        table_pre = pd.crosstab(data['group'], data[col])
        chi2_pre, p_pre, _, _ = chi2_contingency(table_pre)
    except:
        chi2_pre, p_pre = None, None
    # 匹配后统计
    post_high_count, post_high_pct = count_percent(matched_df[matched_df['group']==1][col])
    post_low_count, post_low_pct = count_percent(matched_df[matched_df['group']==0][col])
    try:
        table_post = pd.crosstab(matched_df['group'], matched_df[col])
        chi2_post, p_post, _, _ = chi2_contingency(table_post)
    except:
        chi2_post, p_post = None, None
    stat_result.append({
        '变量': col,
        '匹配前高组频数': pre_high_count, '匹配前高组百分比': pre_high_pct,
        '匹配前低组频数': pre_low_count, '匹配前低组百分比': pre_low_pct,
        '匹配前卡方': chi2_pre, '匹配前p值': p_pre,
        '匹配后高组频数': post_high_count, '匹配后高组百分比': post_high_pct,
        '匹配后低组频数': post_low_count, '匹配后低组百分比': post_low_pct,
        '匹配后卡方': chi2_post, '匹配后p值': p_post
    })

stat_df = pd.DataFrame(stat_result)
stat_df.to_excel('PTM/match_stat_summary_selected.xlsx', index=False)

# 5. 匹配后分析影响因素
factor_analysis = []
for col in covariates_match:
    if col in matched_df.columns:
        if pd.api.types.is_numeric_dtype(matched_df[col]):
            high_mean = matched_df[matched_df['group']==1][col].mean()
            low_mean = matched_df[matched_df['group']==0][col].mean()
            factor_analysis.append({'变量': col, '高压力组均值': high_mean, '低压力组均值': low_mean})
        else:
            factor_analysis.append({'变量': col, '高压力组均值': '非数值型', '低压力组均值': '非数值型'})
factor_df = pd.DataFrame(factor_analysis)
factor_df.to_excel('PTM/factor_analysis.xlsx', index=False)

# 6. 网络分析（以相关性为例）
# 只对数值型变量和学业压力总分做相关性分析
# 网络分析：对匹配后数据的后半部分变量，按高低压力组分别做相关性网络
network_df = df.loc[matched_df.index, covariates_network].copy()
network_df['group'] = matched_df['group'].values
all_num_df = pd.get_dummies(network_df, drop_first=True)
num_cols_net = [col for col in all_num_df.columns if col != 'group']

# 高压力组网络分析
high_df = all_num_df[all_num_df['group']==1]
corr_high = high_df[num_cols_net].corr()
G_high = nx.Graph()
for i in corr_high.columns:
    for j in corr_high.columns:
        if i != j and abs(corr_high.loc[i, j]) > 0.25:
            G_high.add_edge(i, j, weight=abs(corr_high.loc[i, j]), sign=np.sign(corr_high.loc[i, j]))

# 计算节点可预测性指数（R2）
predictability = {}
for node in corr_high.columns:
    others = [col for col in corr_high.columns if col != node]
    if len(others) > 0:
        X = high_df[others]
        y = high_df[node]
        try:
            from sklearn.linear_model import LinearRegression
            reg = LinearRegression().fit(X, y)
            r2 = reg.score(X, y)
        except:
            r2 = 0
        predictability[node] = r2
    else:
        predictability[node] = 0

plt.figure(figsize=(10,10))
pos = nx.spring_layout(G_high)
edges = G_high.edges()
weights = [G_high[u][v]['weight']*8 for u,v in edges]  # 线更粗
styles = ['solid' if G_high[u][v]['sign']>0 else 'dashed' for u,v in edges]
for style in set(styles):
    idx = [i for i, s in enumerate(styles) if s == style]
    nx.draw_networkx_edges(G_high, pos, edgelist=[list(edges)[i] for i in idx], width=[weights[i] for i in idx], style=style, edge_color=[weights[i] for i in idx], edge_cmap=plt.cm.Reds, alpha=0.9)
# 节点外圈填充表示可预测性
node_r2 = [predictability[n] for n in G_high.nodes()]
nx.draw_networkx_nodes(G_high, pos, node_color='white', node_size=900, edgecolors=plt.cm.Blues(node_r2), linewidths=5)
nx.draw_networkx_labels(G_high, pos, font_size=10)
plt.title('高压力组后半变量相关性网络', fontsize=16)
plt.savefig('PTM/network_analysis_high_selected.png', dpi=600, bbox_inches='tight')
plt.close()

# 低压力组网络分析
low_df = all_num_df[all_num_df['group']==0]
corr_low = low_df[num_cols_net].corr()
G_low = nx.Graph()
for i in corr_low.columns:
    for j in corr_low.columns:
        if i != j and abs(corr_low.loc[i, j]) > 0.25:
            G_low.add_edge(i, j, weight=abs(corr_low.loc[i, j]), sign=np.sign(corr_low.loc[i, j]))
# 计算节点可预测性指数（R2）
predictability_low = {}
for node in corr_low.columns:
    others = [col for col in corr_low.columns if col != node]
    if len(others) > 0:
        X = low_df[others]
        y = low_df[node]
        try:
            from sklearn.linear_model import LinearRegression
            reg = LinearRegression().fit(X, y)
            r2 = reg.score(X, y)
        except:
            r2 = 0
        predictability_low[node] = r2
    else:
        predictability_low[node] = 0
plt.figure(figsize=(10,10))
pos = nx.spring_layout(G_low)
edges = G_low.edges()
weights = [G_low[u][v]['weight']*8 for u,v in edges]  # 线更粗
styles = ['solid' if G_low[u][v]['sign']>0 else 'dashed' for u,v in edges]
for style in set(styles):
    idx = [i for i, s in enumerate(styles) if s == style]
    nx.draw_networkx_edges(G_low, pos, edgelist=[list(edges)[i] for i in idx], width=[weights[i] for i in idx], style=style, edge_color=[weights[i] for i in idx], edge_cmap=plt.cm.Greens, alpha=0.9)
node_r2 = [predictability_low[n] for n in G_low.nodes()]
nx.draw_networkx_nodes(G_low, pos, node_color='white', node_size=900, edgecolors=plt.cm.Blues(node_r2), linewidths=5)
nx.draw_networkx_labels(G_low, pos, font_size=10)
plt.title('低压力组后半变量相关性网络', fontsize=16)
plt.savefig('PTM/network_analysis_low_selected.png', dpi=600, bbox_inches='tight')
plt.close()

