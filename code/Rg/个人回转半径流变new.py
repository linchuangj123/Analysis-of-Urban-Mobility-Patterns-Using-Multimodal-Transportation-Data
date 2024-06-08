import pandas as pd
import transbigdata as tbd
import numpy as np
import matplotlib.pyplot as plt
import math
import datetime
from colorama import Fore, Style
from tqdm import tqdm

# 读取数据
print(">----------正在读取数据表")
data = pd.read_csv("C:\\论文编写程序\\第三篇论文编写程序\\实验代码整理\\论文编写程序\\回转半径\\stay_move.csv")
sample_space = 12  # 定义样本空间(h)
# 对“id”列进行规范化处理
data['id'] = pd.factorize(data['id'])[0]
data['stime'] = pd.to_datetime(data['stime'])
id_list = list(data['id'])
id_list = list(set(id_list))
print(">>---------正在定义组件集")


# 定义组件
# 轨迹质心函数
def r_cm(lon_sum, lat_sum, id_size):
    lon_mean = lon_sum / id_size
    lat_mean = lat_sum / id_size
    return lon_mean, lat_mean


# 定义回转半径函数
def r_g(idside, i_lon, i_lat, cm_lon, cm_lat):
    distances = tbd.getdistance(i_lon, i_lat, cm_lon, cm_lat)
    distances_result = distances ** 2
    turning_radius = math.sqrt(distances_result / idside)
    return turning_radius


print(">>>--------开始进入样本空间循环处理")

# 先创建一个DataFrame容器
new_results = pd.DataFrame({"id": [], "stime_cut": [], "etime_cut": [], "id_side": [], "turning_radius": []})

# 样本空间循环处理
for id_lis in tqdm(range(len(id_list))):
    id = id_list[id_lis]
    df_smple = data[data['id'] == id]
    df_smple = df_smple.sort_values(by=['stime'])
    time = list(df_smple['stime'])
    time_smple = list(set(time))

    # 数据分箱子过筛过程
    if len(df_smple) < 3:  # 检查点1
        print(Fore.RED + "-->警告!!:此id样本数据量过小，不足以计算其回转半径：" + Style.RESET_ALL, id)
        continue  # 当样本过小时自动跳转到下一个循环

    tcel = time[0]
    lis_tcel = [time[0]]  # 时间截断容器
    while tcel <= time[len(time) - 1]:
        tcel = tcel + datetime.timedelta(hours=sample_space)  # 时间+sample_tamp(h)
        lis_tcel += [tcel]

    pd_num = len(df_smple) / (len(lis_tcel) - 1)
    if pd_num < 1:  # 检查点2
        print("-->警告！：样本空间过小，可能存在大量空空间样本,若有必要需重新调整sample_space：", id)
    if len(lis_tcel) < 3:
        print(Fore.YELLOW + "-->警告！！:此id下的样本空间总量过少:" + Style.RESET_ALL, id)

    # 开始分箱处理
    id_tb, id_sizetb, space, stime_cut, etime_cut, turning_radius_tb = [], [], [], [], [], []
    for i in range(1, len(lis_tcel)):
        id_box, id_size, elon, elat, cm_lon, cm_lat = [], [], [], [], [], []  # 质心列表容器
        s_date = lis_tcel[i - 1]  # 此处设为0则保留前面所有空间样本的参数,否则样本空间是相对独立的
        e_date = lis_tcel[i]
        df_tsmplpe = df_smple[(df_smple['stime'] >= s_date) & (df_smple['stime'] <= e_date)]

        if len(df_tsmplpe) == 0:
            id_tb += [id]
            id_sizetb += [0]
            stime_cut += [s_date]
            etime_cut += [e_date]
            turning_radius_tb += [0]
            continue

        l_lon = list(df_tsmplpe['elon'])
        l_lat = list(df_tsmplpe['elat'])
        elon += l_lon
        elat += l_lat

        # 流变质心处理
        total_elon = df_tsmplpe['elon'].sum()
        total_elat = df_tsmplpe['elat'].sum()
        z = len(df_tsmplpe)
        centre_lon, centre_lat = r_cm(total_elon, total_elat, z)

        for num in range(z):
            id_size += [z]
            cm_lon += [centre_lon]
            cm_lat += [centre_lat]
            id_box += [id]

        for nu in range(z):
            turning_radius = r_g(id_size[nu], elon[nu], elat[nu], cm_lon[nu], cm_lat[nu])
            turning_radius_tb += [turning_radius]
            space += [i - 1]
            id_tb += [id]
            id_sizetb += [z]
            stime_cut += [s_date]
            etime_cut += [e_date]

    new_df = pd.DataFrame({
        "id": id_tb,
        "id_side": id_sizetb,
        "stime_cut": stime_cut,
        "etime_cut": etime_cut,
        "turning_radius": turning_radius_tb
    })
    new_results = pd.concat([new_results, new_df], ignore_index=True)

new_results = new_results.groupby(['id', 'stime_cut', 'etime_cut'])['turning_radius'].mean().reset_index()

# 创建一个新列'space'，并为每个id的每个时间窗口分配一个编号
new_results['space'] = new_results.groupby('id').cumcount() + 1

# 保存数据到 CSV 文件
new_results.to_csv(r'Turning_radius.csv', index=False)

# 绘制Turning_radius图
for userid in id_list:
    df_userid = new_results[new_results['id'] == userid]
    df_userid = df_userid[df_userid['turning_radius'] != 0]  # Filter out points where turning radius is 0
    plt.figure(figsize=(10, 5))
    plt.plot(df_userid['space'], df_userid['turning_radius'], label=f'ID: {userid}', marker='o', linestyle='-', color='#00868B')
    plt.xlabel('Time Length')
    plt.ylabel('Turning Radius')
    plt.title(f'Turning Radius for UserID {userid}')
    plt.xscale('log')  # Set y-axis scale to logarithmic
    plt.yscale('log')  # Set y-axis scale to logarithmic
    plt.legend()
    plt.savefig(f'C:\\论文编写程序\\第三篇论文编写程序\\实验代码整理\\论文编写程序\\回转半径\\Rg\\Turning_radius_ID_{userid}.png')  # Modified path to save images
    plt.close()




