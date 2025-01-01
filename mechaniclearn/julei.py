import numpy as np
from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import linkage, fcluster, dendrogram
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# 定义5个平面坐标
coordinates = np.array([[0, 2],[0, 0],[1, 0],[5, 0],[5, 2]])

# 计算欧氏距离矩阵
distance_matrix = pdist(coordinates, metric='euclidean')
# 将距离矩阵转换为平方形式
square_distance_matrix = squareform(distance_matrix)
print("Square Form Distance Matrix:")
print(square_distance_matrix)

# Square Form Distance Matrix:
# [[0.         2.         2.23606798 5.38516481 5.        ]     
#  [2.         0.         1.         5.         5.38516481]     
#  [2.23606798 1.         0.         4.         4.47213595]     
#  [5.38516481 5.         4.         0.         2.        ]     
#  [5.         5.38516481 4.47213595 2.         0.        ]]  

# 进行层次聚类
Z = linkage(square_distance_matrix, method='complete')

# 停止聚类到两个类
num_clusters = 2
clusters = fcluster(Z, num_clusters, criterion='maxclust')

# 输出聚类结果
for i, cluster in enumerate(clusters):
    print(f"Point {i+1} belongs to cluster {cluster}")

# Point 1 belongs to cluster 2
# Point 2 belongs to cluster 2
# Point 3 belongs to cluster 2
# Point 4 belongs to cluster 1
# Point 5 belongs to cluster 1

# 计算每个类的中心
cluster_centers = []
for cluster_id in np.unique(clusters):
    cluster_points = coordinates[clusters == cluster_id]
    center = np.mean(cluster_points, axis=0)
    cluster_centers.append(center)

# 选择每个类中与类中心距离最近的点作为初始类中心
initial_centers = []
for i, center in enumerate(cluster_centers):
    distances = np.linalg.norm(coordinates[clusters == (i + 1)] - center, axis=1)
    closest_point_index = np.argmin(distances)
    closest_point = coordinates[clusters == (i + 1)][closest_point_index]
    initial_centers.append(closest_point)

# 应用K均值聚类算法
kmeans = KMeans(n_clusters=num_clusters, init=np.array(initial_centers), n_init=1)
kmeans.fit(coordinates)

# 输出K均值聚类结果
for i, label in enumerate(kmeans.labels_):
    print(f"Point {i+1} belongs to cluster {label + 1}")

# Point 1 belongs to cluster 2
# Point 2 belongs to cluster 2
# Point 3 belongs to cluster 2
# Point 4 belongs to cluster 1
# Point 5 belongs to cluster 1

# 创建一个包含两个子图的窗口
fig, axs = plt.subplots(1, 2, figsize=(15, 5))

# 绘制层次聚类的树状图
axs[0].set_title("Hierarchical Clustering Dendrogram")
dendrogram(Z, labels=[f'Point {i+1}' for i in range(len(coordinates))], ax=axs[0])
axs[0].set_xlabel("Points")
axs[0].set_ylabel("Distance")

# 绘制K均值聚类结果
axs[1].set_title("K-Means Clustering Result")
axs[1].scatter(coordinates[:, 0], coordinates[:, 1], c=kmeans.labels_, cmap='viridis', marker='o')
axs[1].scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], c='red', marker='x', s=100)
axs[1].set_xlabel("X Coordinate")
axs[1].set_ylabel("Y Coordinate")

# 显示图形
plt.tight_layout()
plt.show()