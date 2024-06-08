import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm.auto import tqdm

# 设置随机种子以保证结果的可复现性
np.random.seed(0)

# 读取数据
file_path = 'C:/论文编写程序/第三篇论文编写程序/实验代码整理/论文编写程序/BM/visit_duration_distance_v_all.csv'  # 注意路径中的斜杠
df = pd.read_csv(file_path)

# 转换时间格式并排序
df['stime'] = pd.to_datetime(df['stime'])
df = df.sort_values(by='stime')

# 准备输出路径
output_path = 'C:/论文编写程序/第三篇论文编写程序/实验代码整理/论文编写程序/BM/BM图'  # 注意路径中的斜杠

# 获取所有唯一的userid
unique_userids = df['id'].unique()

# 定义颜色
edgeColors = np.array([
    [255/255, 128/255, 0/255],  # 深橙色
    [0/255, 153/255, 153/255]   # 深青色
])

fillColors = edgeColors * 0.7 + 1 * 0.3  # 使填充颜色比边界颜色浅
transparency = 0.5  # 透明度

for userid in tqdm(unique_userids, desc="Processing UserIDs"):
    df_user = df[df['id'] == userid]

    # 仅在用户有足够数据时继续
    if len(df_user) < 2:
        continue

    # 获取用户的时间戳并计算差值
    timestamps = df_user['stime']
    time_diffs = timestamps.diff().dt.total_seconds().dropna()

    # 确保有足够的时间间隔进行计算
    if len(time_diffs) < 2:
        continue

    # 初始化存储列表
    B_values = []
    M_values = []
    time_labels = []

    # 获取起始时间点
    start_time = df_user['stime'].iloc[0]

    epsilon = 1e-10  # 避免除以零
    for i in range(2, len(time_diffs) + 1):
        subset = time_diffs.iloc[:i]
        mean = subset.mean()
        std = subset.std() + epsilon  # 修正标准差以避免除以零的错误

        # 计算B值
        B = (std - mean) / (std + mean)

        # 修正后的M值计算
        M_numerator = sum([
            (subset.iloc[j-1] - subset[:j].mean()) * (subset.iloc[j] - subset[:j+1].mean())
            for j in range(1, len(subset))
        ])
        M_denominator = sum([
            (subset.iloc[j-1] - subset[:j].mean())**2
            for j in range(1, len(subset))
        ]) + epsilon  # 避免除以零
        M = M_numerator / M_denominator

        B_values.append(B)
        M_values.append(M)
        # 保存时间长度而不是具体的时间戳
        time_labels.append((timestamps.iloc[i-1] - start_time).total_seconds() / (60*60*24))  # 单位转换为小时

    # 绘图
    plt.figure(figsize=(10, 5))
    plt.plot(time_labels, B_values, label='B Value', color=edgeColors[1], marker='o', linestyle='--', markerfacecolor=fillColors[1], alpha=transparency)
    plt.plot(time_labels, M_values, label='M Value', color=edgeColors[0], marker='o', linestyle='--', markerfacecolor=fillColors[0], alpha=transparency)
    plt.xlabel('Time(24h)')
    plt.ylabel('BM Values')
    plt.legend()
    #plt.grid(True)

    # 保存图像
    plt.savefig(f"{output_path}/BM_Analysis_UserID_{userid}_Time_Elapsed.png")
    plt.close()
