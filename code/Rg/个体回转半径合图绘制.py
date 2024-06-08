import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

# 读取数据
data = pd.read_csv("C:\\论文编写程序\\第三篇论文编写程序\\实验代码整理\\论文编写程序\\回转半径\\Turning_radius.csv")

# 指定要绘制的用户ID
selected_ids = [4, 14, 17, 66]

# 定义颜色
colors = [
    '#009999',  # 深青色
    '#800080',  # 深紫色
    '#CC0066',  # 深粉色
    '#FF8000'   # 深橙色
]

# 绘制Turning_radius图
plt.figure(figsize=(12, 8))
for idx, userid in enumerate(selected_ids):
    df_userid = data[data['id'] == userid]
    df_userid = df_userid[df_userid['turning_radius'] != 0]  # 过滤掉turning_radius为0的点

    # 检查数据点数量
    if len(df_userid) <= 15:
        continue

    plt.plot(df_userid['space'], df_userid['turning_radius'], label='ID', marker='o', linestyle='-',
             color=colors[idx], markerfacecolor=colors[idx], alpha=0.5)

plt.xlabel('Time(12h)')
plt.ylabel('Turning Radius')
# plt.title('Turning Radius for Selected UserIDs')
plt.xscale('log')  # 设置x轴为对数尺度
plt.yscale('log')  # 设置y轴为对数尺度
plt.legend()
# plt.grid(True)
# 保存图像
plt.savefig(f'C:\\论文编写程序\\第三篇论文编写程序\\实验代码整理\\论文编写程序\\回转半径\\Rg\\Turning_radius_Selected_Users.png')
plt.show()

