# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pylab 
import statsmodels.api as sm
import scipy.stats as stats

#读取数据
df = pd.read_csv('USvideos.csv', low_memory=False)
#dfnfl = pd.read_csv('NFL Play by Play 2009-2017 (v4).csv', low_memory=False)
#数值属性筛选
label_shuzhi = ['views',
                'likes',
                'dislikes',
                'comment_count']
#数值属性数据
df_shuzhi = df[label_shuzhi]
#数据摘要-----------
#属性可能取值频数
def frequ(dfcolumn):
    frequdf = df[dfcolumn].value_counts()
    frequdf = pd.DataFrame(frequdf)
    return frequdf
#输出标称属性可能取值的频数列表
def nafrequ():
    print('category_id可能取值的频数:')
    print(frequ('category_id'))
    print('comments_disabled可能取值的频数:')
    print(frequ('comments_disabled'))
    print('ratings_disabled可能取值的频数:')
    print(frequ('ratings_disabled'))
    print('video_error_or_removed可能取值的频数:')
    print(frequ('video_error_or_removed'))
#    print(frequnfl('PlayType'))

#数据缺失统计
def lostdata(dataf):
    nulltotal = dataf.isnull().sum().sort_values(ascending=False)
    return nulltotal
#输出数值属性缺失值
def numnull(shuzhi):
    print('数值属性缺失值：',)
    print(lostdata(shuzhi))
#    print(lostdata(dfnfl[['PosTeamScore']]))

#数值属性最大值
def nummax(shuzhi):
    print('数值属性最大值：',)
    print(shuzhi.max())
    
#数值属性最小值
def nummin(shuzhi):
    print('数值属性最小值：',)
    print(shuzhi.min())
    
#数值属性均值
def nummean(shuzhi):
    print('数值属性均值：',)
    print(shuzhi.mean())
    
#数值属性中位数
def nummed(shuzhi):
    print('数值属性中位数：',)
    print(shuzhi.median())
    
#数值属性四分位数
def numqua(shuzhi):
#    functions = ['25%', '50%', '75%']
    numup = shuzhi.quantile(0.25)
    nummed = shuzhi.quantile(0.5)
    numdow = shuzhi.quantile(0.75)
    numup = pd.DataFrame(numup)
    nummed = pd.DataFrame(nummed)
    nummdow = pd.DataFrame(numdow)
    fournum = pd.merge(numup,nummed,left_index=True,right_index=True)
    fournum = pd.merge(fournum,nummdow,left_index=True,right_index=True)
#print(numup.index,numup.columns)
#,df_shuzhi.quantile(0.5),df_shuzhi.quantile(0.75)].agg(functions)
    print('数值属性四分位数：',)
    print(fournum)
#数据可视化--------------    
#数值属性直方图+qq图
def histog(dataf):
    dataf.hist(bins = 50)
    plt.show()
    sm.qqplot(dataf,line='45')
    pylab.show()
    
#盒图绘制
def boxplot(dataf):
    dataf.boxplot()
    plt.show()
    
#sample_size = df[['Number of Existing Stories','Current Status']]
#sample_size.boxplot(by='Current Status')
#plt.xticks(rotation=90)
#缺失值处理
#1将缺失部分剔除
def dropnull(dataf):
    datafno = dataf.dropna()
    histog(dataf)
    histog(datafno)
    
#2用最高频率值来填补缺失值
def modefill(dataf):
    modedt = dataf.mode()#获取众数
#    print(modedt)
    modedata = modedt.iloc[0,0]#众数值提取
    print(modedata)
    datamf = dataf.fillna(modedata)#填充
    histog(dataf)
    histog(datamf)
    # datamf.to_csv('modefill.csv')
#    datamax = dataf.fillna(dataf.max())
#    histog(datamax)
#from scipy.stats import ttest_rel
#from scipy import stats
#testdata = df[['Existing Units']]
#filldata = df['Proposed Units']
#okdata = testdata.fillna(filldata)
#testdata.to_csv('a1.csv')
#okdata.to_csv('a2.csv')
#3通过属性的相关关系来填补缺失值
#3.1数值属性相关关系
def corrsp(dataf):
    cs = dataf.corr()
    cs.to_csv('corr.csv')
    print(cs)
    print('EOF')
    return
#根据相关性填充    
def corfill(dataf,clone,cltwo):
    datatemp = dataf
    datatemp[clone] = datatemp.apply(lambda x: x[cltwo] if pd.isnull(x[clone]) else x[clone],axis=1)
    datatemp[cltwo] = datatemp.apply(lambda x: x[clone] if pd.isnull(x[cltwo]) else x[cltwo],axis=1)
    # datatemp.to_csv('corfill.csv')
    print('EOF')
    histog(dataf[[clone]])
    histog(datatemp[[clone]])
    histog(dataf[[cltwo]])
    histog(datatemp[[cltwo]])
#4数据对象之间的相似性来填补缺失值
#4.1相似性

from math import sqrt 
def sim_dist(preb,clone,cltwo):
    preb = preb.dropna()
    si = {}
    for it in preb[clone]:
        if it in preb[cltwo]:
            si[it] = 1
            if len(si) == 0:
                return 0
    totalsum = sum([pow(preb[clone][item]-preb[cltwo][item],2) for item in preb[clone] if item in preb[clone]])
    return 1/(1+sqrt(totalsum))
#df_shuzhi['Existing Units'] = df_shuzhi.apply(lambda x: x['Proposed Units'] if pd.isnull(x['Existing Units']) else x['Existing Units'],axis=1)
#df_shuzhi.to_csv('a3.csv')
if __name__ == "__main__":
#    print(df.dtypes)
#    nafrequ()
#    nummax(df_shuzhi)
#    nummin(df_shuzhi)
#    nummean(df_shuzhi)
#    nummed(df_shuzhi)
#    numqua(df_shuzhi)
#    numnull(df_shuzhi)

#    histog(df[['views']])
#    histog(df[['likes']])
#    histog(df[['dislikes']])
   histog(df[['comment_count']])

   boxplot(df[['views']])
   boxplot(df[['likes']])
   boxplot(df[['dislikes']])
   boxplot(df[['comment_count']])

   dropnull(df_shuzhi)

   modefill(df_shuzhi)

   corrsp(df_shuzhi)#输出相关性
   corfill(df_shuzhi,'views','likes')#根据相关性填充
    
    # print(sim_dist(df_shuzhi,'price','points'))