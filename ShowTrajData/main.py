import pandas as pd
import torch
import numpy as np
import torch.nn.functional as F
import seaborn as sns
import matplotlib.pyplot as plt
from DynamicTimeWarpingLoop import DynamicTimeWarping
from functools import cache
from tqdm import tqdm

def edit_distance(x, y):
    m, n = len(x), len(y)
    dp = np.zeros((m + 1, n + 1))
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif x[i - 1] == y[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
    return dp[m][n]

'''
类内热力图
'''  
def in_com():
    flist=[]
    for i in tqdm(range(0,20)):
        data1="./data/results/front/0-%s.cell"%(i)
        traj1 = torch.tensor(np.loadtxt(data1,delimiter='\t'))
        fli=[]
        for j in range(0,20):
            data2="./data/results/front/0-%s.cell"%(j)
            traj2 = torch.tensor(np.loadtxt(data2,delimiter="\t"))
            if(traj1.shape[0] > traj2.shape[0]):
                a = traj1[:traj2.shape[0],:]
                b= traj2
            else:
                a= traj1
                b = traj2[:traj1.shape[0],:]
            fli.append(round(F.cosine_similarity(a, b, dim=0)[1].item(),2))
        flist.append(fli)
    flist=np.array(flist)
    sns.set_style('whitegrid', {'font.sans-serif': ['simhei','FangSong']})
    plt.figure(figsize=(11, 11))
    ax=sns.heatmap(flist,
            annot=True,  # 显示相关系数的数据
            center=0.5,  # 居中
            fmt='.2f',  # 只显示两位小数
            linewidth=0.5,  # 设置每个单元格的距离
            linecolor='blue',  # 设置间距线的颜色
            vmin=0, vmax=1,  # 设置数值最小值和最大值
            xticklabels=True, yticklabels=True,  # 显示x轴和y轴
            square=True,  # 每个方格都是正方形
            cbar=True,  # 绘制颜色条
            cmap='coolwarm_r',  # 设置热力图颜色
            )
    ax.set_title("front-0类类内相似度")
    #plt.show()
    plt.savefig("front-0类内热力图.png",dpi=600)
    
'''
类间热力图
''' 
def out_com():
    flist=[]
    for i in tqdm(range(0,20)):
        data1="./data/results/tamaraw/0-%s.cell"%(i)
        traj1 = torch.tensor(np.loadtxt(data1,delimiter='\t'))
        fli=[]
        for j in range(0,20):
            data2="./data/results/tamaraw/1-%s.cell"%(j)
            traj2 = torch.tensor(np.loadtxt(data2,delimiter="\t"))
            if(traj1.shape[0] > traj2.shape[0]):
                a = traj1[:traj2.shape[0],:]
                b= traj2
            else:
                a= traj1
                b = traj2[:traj1.shape[0],:]
            fli.append(round(F.cosine_similarity(a, b, dim=0)[1].item(),2))
        flist.append(fli)
    flist=np.array(flist)
    sns.set_style('whitegrid', {'font.sans-serif': ['simhei','FangSong']})
    plt.figure(figsize=(11, 11))
    ax=sns.heatmap(flist,
            annot=True,  # 显示相关系数的数据
            center=0.5,  # 居中
            fmt='.2f',  # 只显示两位小数
            linewidth=0.5,  # 设置每个单元格的距离
            linecolor='blue',  # 设置间距线的颜色
            vmin=0, vmax=1,  # 设置数值最小值和最大值
            xticklabels=True, yticklabels=True,  # 显示x轴和y轴
            square=True,  # 每个方格都是正方形
            cbar=True,  # 绘制颜色条
            cmap='coolwarm_r',  # 设置热力图颜色
            )
    ax.set_title("tamaraw-0-1类类间相似度")
    plt.savefig("tamaraw-0-1类间热力图.png",dpi=600)    

'''
小提琴图
'''
def box_in_com():
    data=["./data/data/","./data/results/wtfpad_0821_1454/","./data/results/front/","./data/results/tamaraw/"]
    flist=[]
    for k in tqdm(data):
        fli=[]
        for i in range(0,90):
            data1=k+"0-%s.cell"%(i)
            traj1 = torch.tensor(np.loadtxt(data1,delimiter='\t'))
            for j in range(i+1,90):
                data2=k+"1-%s.cell"%(j)
                traj2 = torch.tensor(np.loadtxt(data2,delimiter="\t"))
                if(traj1.shape[0] > traj2.shape[0]):
                    a = traj1[:traj2.shape[0],:]
                    b= traj2
                else:
                    a= traj1
                    b = traj2[:traj1.shape[0],:]
                fli.append(round(F.cosine_similarity(a, b, dim=0)[1].item(),2))
        flist.append(fli)
    labels=["raw","wtfpad","front","tamaraw"]
    sns.set_style('whitegrid', {'font.sans-serif': ['simhei','FangSong']})
    ax=sns.violinplot(flist)
    ax.set_title("类间相似度")
    ax.set_xticks(range(len(data)))
    ax.set_xticklabels(labels)
    ax.yaxis.grid(True)
    ax.set_xlabel("class")
    ax.set_ylabel("Similarity")
    plt.savefig("类间小提琴图.png")
    plt.show()

    
if __name__ == '__main__':
    #out_com()
    #out_com()
    #box_in_com()

    # data1="./data/results/wtfpad_0821_1454/0-0.cell"
    # data2="./data/results/wtfpad_0821_1454/0-2.cell"
    # data1="./data/data/0-0.cell"
    # data2="./data/data/0-1.cell"
    # traj1 = torch.tensor(np.loadtxt(data1,delimiter='\t'))


    # traj2 = torch.tensor(np.loadtxt(data2,delimiter="\t"))

    # if(traj1.shape[0] > traj2.shape[0]):
    #     a = traj1[:traj2.shape[0],:]
    #     b= traj2
    # else:
    #     a= traj1
    #     b = traj2[:traj1.shape[0],:]

    

    # print("****%s与%s****"%(data1.split('/')[-1],data2.split('/')[-1]))

    # print("余弦相似度：",round(F.cosine_similarity(a, b, dim=0)[1].item(),2))

    # print("编辑距离：",round(edit_distance(a[:,1], b[:,1]),2))

    # print("曼哈顿距离: ",round(F.pairwise_distance(a[:,1], b[:,1], p=1,eps=1e-6).item(),2))

    # print("欧氏距离: ",round(F.pairwise_distance(a[:,1], b[:,1], p=2,eps=1e-6).item(),2))

    # print("DTW距离: ",round(DynamicTimeWarping(traj1, traj2)[0],2))



