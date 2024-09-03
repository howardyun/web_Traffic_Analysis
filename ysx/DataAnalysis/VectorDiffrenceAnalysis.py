import pandas as pd
import numpy as np
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
import matplotlib.pyplot as plt

x = np.array([1, 2, 3, 4, 5], dtype='float')
print(x)
y = np.array([2, 3, 4], dtype='float')

print(fastdtw(x, y))

# 读取数据
file_path = '../collectData/RawDataWithoutAnyProtection_Https/csv/cctv.com_packets.csv'
data = pd.read_csv(file_path)

# 提取size列作为流量数据
traffic_data = data['size'].values

# 确保流量数据是一维向量
traffic_data = traffic_data.flatten()

# 滑动窗口参数
window_size = 50
step_size = 10

# 提取滑动窗口特征
windows = []
for i in range(0, len(traffic_data) - window_size + 1, step_size):
    window = traffic_data[i:i + window_size].flatten().tolist()  # 展平窗口并转换为列表
    windows.append(window)

# 验证窗口形状
print(f"Number of windows: {len(windows)}")
print(windows[0])

# 计算窗口之间的DTW距离
distances = np.zeros((len(windows), len(windows)))
for i in range(len(windows)):
    for j in range(i + 1, len(windows)):
        print(f"Calculating DTW distance between windows {i} and {j}")
        distance, _ = fastdtw(np.array(windows[i], dtype='float'), np.array(windows[j], dtype='float'))
        distances[i, j] = distance

# 可视化DTW距离矩阵
plt.imshow(distances, cmap='hot', interpolation='nearest')
plt.colorbar()
plt.title('DTW Distance Matrix')
plt.show()

# 找出最相似的窗口
min_distance = np.min(distances[np.nonzero(distances)])
indices = np.where(distances == min_distance)
print(f"Most similar windows are: {indices[0][0]} and {indices[1][0]} with distance {min_distance}")
