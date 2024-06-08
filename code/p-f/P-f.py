import pandas as pd
import matplotlib.pyplot as plt

# 从CSV文件读取数据
data = pd.read_csv('C:\\论文编写程序\\第二篇论文编写程序\\p-r code\\destination_r_f.csv')
f = data["f"]

# 计算最小值和最大值
min_f = f.min()
max_f = f.max()

# 根据最小值和最大值平均分成50个bins
bins = pd.interval_range(start=min_f, end=max_f, periods=50)

# 分箱
gb = pd.cut(f, bins)
x = pd.value_counts(gb, sort=False)

# 计算每个分箱中的人数占总人数的概率
total_count = len(f)
probabilities = x / total_count

# 绘制双对数坐标系散点图
plt.figure(figsize=(10, 6))
plt.scatter([b.left for b in bins], probabilities, s=150, alpha=0.7)
plt.xscale('log')
plt.yscale('log')
plt.xlabel('f')
plt.ylabel('P')
plt.title('P-f')
plt.grid(True)
plt.show()

