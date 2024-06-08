import pandas as pd
import transbigdata as tbd
import numpy as np
import matplotlib.pyplot as plt
import math
import datetime
from colorama import Fore, Style
from tqdm import tqdm

# 读取数据
data = pd.read_csv("C:\\论文编写程序\\第三篇论文编写程序\\实验代码整理\\论文编写程序\\回转半径\\Turning_radius.csv")
id_list = list(data['id'])
id_list = list(set(id_list))

# 定义颜色
edgeColors = np.array([
    [0 / 255, 134 / 255, 139 / 255],  # 深青色
])
fillColors = edgeColors * 0.7 + 1 * 0.3  # 使填充颜色比边界颜色浅
transparency = 0.5  # 透明度

# 绘制Turning_radius图
for userid in tqdm(id_list, desc="Processing UserIDs"):
    df_userid = data[data['id'] == userid]
    df_userid = df_userid[df_userid['turning_radius'] != 0]  # 过滤掉turning_radius为0的点

    # 检查数据点数量
    if len(df_userid) <= 30:
        continue

    plt.figure(figsize=(10, 5))
    plt.plot(df_userid['space'], df_userid['turning_radius'], label=f'ID: {userid}', marker='o', linestyle='-',
             color=edgeColors[0], markerfacecolor=fillColors[0], alpha=transparency)
    plt.xlabel('Time Length')
    plt.ylabel('Turning Radius')
    plt.title(f'Turning Radius for UserID {userid}')
    plt.xscale('log')  # 设置x轴为对数尺度
    plt.yscale('log')  # 设置y轴为对数尺度
    plt.legend()
    plt.savefig(f'C:\\论文编写程序\\第三篇论文编写程序\\实验代码整理\\论文编写程序\\回转半径\\Rg\\Turning_radius_ID_{userid}.png')  # 修改路径以保存图片
    plt.close()

