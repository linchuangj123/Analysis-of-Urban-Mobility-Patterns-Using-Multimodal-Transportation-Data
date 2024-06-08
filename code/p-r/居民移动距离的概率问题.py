import pandas as pd
import math
import matplotlib.pyplot as plt
# 从CSV文件读取数据
data = pd.read_csv('C:\\花旗共享单车\\202401-citibike-tripdata_1.csv')

# 提取经度和纬度数据
s_lat = data['start_lat'].tolist()
s_lng = data['start_lng'].tolist()
e_lat = data['end_lat'].tolist()
e_lng = data['end_lng'].tolist()

# 计算距离
earth_radius = 6370.856

def ab_distance(a_lat, a_lng, b_lat, b_lng):
    lat_dis = abs(a_lat - b_lat) * math.pi * earth_radius / 180
    lng_dis = abs(a_lng - b_lng) * math.pi * earth_radius * math.cos((a_lat + b_lat) * math.pi / 360) / 180
    return math.sqrt(lat_dis ** 2 + lng_dis ** 2) * 1000

distance_result = [ab_distance(s_lat[i], s_lng[i], e_lat[i], e_lng[i]) for i in range(len(s_lat))]

# 分箱距离
bins = [i * 50 for i in range(201)]
gb = pd.cut(distance_result, bins)
x = pd.value_counts(gb)
# 计算每个分箱中的人数占总人数的概率，并将概率从大到小排序
total_count = len(distance_result)
probabilities = x / total_count
probabilities_sorted = probabilities.sort_values(ascending=False)

# 绘制双对数坐标系散点图
plt.figure(figsize=(10, 6))
plt.scatter(bins[:-1], probabilities_sorted, s=150, alpha=0.7)
plt.xscale('log')
plt.yscale('log')
plt.xlabel('r')
plt.ylabel('P')
plt.title('P-r')
plt.grid(True)
plt.show()
