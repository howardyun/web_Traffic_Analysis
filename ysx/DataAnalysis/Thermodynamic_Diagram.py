import os
import pandas as pd
import numpy as np
from scipy.spatial.distance import euclidean, cityblock
from scipy.stats import pearsonr
from sklearn.metrics.pairwise import cosine_similarity
import seaborn as sns
import matplotlib.pyplot as plt

# 文件夹路径
folder_path = '../collectData/RawDataWithoutAnyProtection_Https/csv/'

# 获取所有csv文件
file_list = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.csv')]

# 初始化相似度矩阵
num_files = len(file_list)
euclidean_matrix = np.zeros((num_files, num_files))
manhattan_matrix = np.zeros((num_files, num_files))
cosine_matrix = np.zeros((num_files, num_files))
pearson_matrix = np.zeros((num_files, num_files))


# 定义计算相似度的函数
def calculate_similarity(file_a, file_b, max_length):
    data_a = pd.read_csv(file_a)
    data_b = pd.read_csv(file_b)

    data_a['timestamp'] = pd.to_datetime(data_a['timestamp'], unit='s')
    data_a.set_index('timestamp', inplace=True)
    data_a = data_a.resample('S').sum().fillna(0)
    flow_vector_a = data_a['size'].values

    data_b['timestamp'] = pd.to_datetime(data_b['timestamp'], unit='s')
    data_b.set_index('timestamp', inplace=True)
    data_b = data_b.resample('S').sum().fillna(0)
    flow_vector_b = data_b['size'].values

    # 确保向量长度一致
    if len(flow_vector_a) < max_length:
        flow_vector_a = np.pad(flow_vector_a, (0, max_length - len(flow_vector_a)), 'constant')
    if len(flow_vector_b) < max_length:
        flow_vector_b = np.pad(flow_vector_b, (0, max_length - len(flow_vector_b)), 'constant')
    if len(flow_vector_a) > max_length:
        flow_vector_a = flow_vector_a[:max_length]
    if len(flow_vector_b) > max_length:
        flow_vector_b = flow_vector_b[:max_length]

    euclidean_distance = euclidean(flow_vector_a, flow_vector_b)
    manhattan_distance = cityblock(flow_vector_a, flow_vector_b)
    cosine_sim = cosine_similarity([flow_vector_a], [flow_vector_b])[0][0]
    pearson_corr, _ = pearsonr(flow_vector_a, flow_vector_b)

    return euclidean_distance, manhattan_distance, cosine_sim, pearson_corr


# 确定最长的向量长度
max_length = 0
for file in file_list:
    data = pd.read_csv(file)
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='s')
    data.set_index('timestamp', inplace=True)
    data = data.resample('S').sum().fillna(0)
    max_length = max(max_length, len(data))

# 计算相似度并填充矩阵
for i in range(num_files):
    for j in range(num_files):
        if i != j:
            euclidean_distance, manhattan_distance, cosine_sim, pearson_corr = calculate_similarity(file_list[i],
                                                                                                    file_list[j],
                                                                                                    max_length)
            euclidean_matrix[i, j] = euclidean_distance
            manhattan_matrix[i, j] = manhattan_distance
            cosine_matrix[i, j] = cosine_sim
            pearson_matrix[i, j] = pearson_corr


# 画热力图
def plot_heatmap(matrix, title):
    plt.figure(figsize=(10, 8))
    sns.heatmap(matrix, annot=False, fmt=".2f", cmap="viridis")
    plt.title(title)
    plt.show()


# 绘制热力图
plot_heatmap(euclidean_matrix, 'Euclidean Distance Heatmap')
plot_heatmap(manhattan_matrix, 'Manhattan Distance Heatmap')
plot_heatmap(cosine_matrix, 'Cosine Similarity Heatmap')
plot_heatmap(pearson_matrix, 'Pearson Correlation Heatmap')
