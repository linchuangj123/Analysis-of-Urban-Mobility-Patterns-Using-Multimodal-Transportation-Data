import pandas as pd
import math
import transbigdata as tbd
import seaborn as sns
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
"此代码职能如下：" \
"计算μ，计算c"
"完成城市空间吸引力μ与人群移动行为成本c之间的关系"
"可视化μ-c关系图"

#计算城市空间吸引力μ
#参数设置
file="destination_r_f.csv"#取得频率以及拜访量
eta=2                  #自定义参数
sigma=500
bounds=[-178, 1, 179, 65]#原始处理坐标范围
params = tbd.area_to_params(bounds,accuracy=500)#原始栅格参数

#读取数据
path=r"C:\论文编写程序\第三篇论文编写程序\实验代码整理\论文编写程序\城市空间吸引力\{}".format(file)
df_gc=pd.read_csv(path)
N,f,r=list(df_gc['visit_count']),list(df_gc['f']),list(df_gc['mean_distance'])

#吸引力模型u=N/A*(fr)**eta
μ=[]
for i in range(len(df_gc)):
    μ+=[(N[i]/2*math.pi*sigma*((r[i]*f[i])*eta))]
df_gc['attraction']=μ
print(df_gc)
#保存为新的csv文件
df_gc.to_csv('urban_attraction.csv', index=False)
