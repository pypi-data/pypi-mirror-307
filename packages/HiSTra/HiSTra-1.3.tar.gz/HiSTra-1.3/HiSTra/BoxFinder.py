#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" All functions are used for finding potential translocation chromosome pairs, the potential position on the chromosomes.

Available functions:
- eigen_calculation:
- eigen_output:
- outlier:
- compare_evalue
"""
import sys
import getopt
import os
import fnmatch
import random
import itertools

import numpy as np
import pandas as pd
import scipy.stats as st

from datetime import *
from scipy import sparse
from random import sample

import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches
from matplotlib_venn import venn2,venn3,venn3_circles,venn2_circles
import seaborn as sns

from HiSTra.utils import *
from HiSTra.SparseMatrixDeal import sparse_matrix_in

def chromoTLPairsNumber(sample_df, result_path='.', cutoff=0.6):
    """
    Input:
        - sample_df: a dataframe of 253 chromosome pairs with sorted score.
        - result_path: ../SV_result/sample_name
    """
    result_path = os.path.abspath(result_path)
    tmp = sample_df[sample_df.Score>0]
    plt.figure(figsize=(15,10))
    tmp['Score'].plot(style='-o')
    plt.ylabel('SV score')
    plt.tick_params(labelsize=15)
    
    if len(tmp)<30:
        plt.savefig(os.path.join(result_path,'baselinechoose.png'),dpi=400)
        return len(tmp)
    else:
        cum = tmp['Score'].cumsum()/tmp['Score'].sum()
        cum.plot(color='r',secondary_y=True,style='-o',linewidth=2)
        plt.axhline(y = cutoff, c= 'g', ls = '--', lw =2)
        plt.axvline(x = len(cum[cum<cutoff]) , c= 'g', ls = '--', lw =2)
        plt.text(len(cum[cum<cutoff]), 0, str(len(cum[cum<cutoff])), ha='center', va='bottom',fontsize=15)
        plt.tick_params(labelsize=15)
        plt.savefig(os.path.join(result_path,'baselinechoose.png'),dpi=400)
        return len(cum[cum<cutoff])

    
def deDoc_createInputMatrix(MMT,dirname,chr1,chr2,resolution):
    """Save covariance matrix as deDoc input files.
    Input:
        - MMT, covariance matrix.
        - dirname, ../matrix_aligned/sample_name
        - chr1, chr2, the chromosome pairs.
        - resolution, '500k' or '100k', determine the savepath is dirname/square_*00k/chr1_in_chr1_chr2.txt
    Return:
        None.
    """
    X1 = sparse.coo_matrix(MMT)
    col =np.int64( X1.col + 1)
    row = np.int64(X1.row + 1)
    data = X1.data
    X1 = np.array([col,row,data]).T
    
    deDoc_in_dir = os.path.join(dirname,'_'.join(["square",resolution]))
#     print(deDoc_in_dir)
    folder = os.path.exists(deDoc_in_dir)
    if not folder:
        os.makedirs(deDoc_in_dir)
        print(f"--- Create new deDoc folder in {deDoc_in_dir}... ---")
    filename = os.path.join(deDoc_in_dir, chr1+'_in_'+chr1+'_'+chr2+'.txt')
    if not os.path.exists(filename):
        np.savetxt(filename,X1,fmt='%d %d %.1lf',header=str(len(X1.data)),comments='')
    
def deDoc_in_pre(dirname,sample_df, res_unit, cutoff=0.6):
    """
    Input:
        - dirname: ../Matrix_aligned/Sample_name/100k
        - sample_df: chromosome pairs with sorted score
        - cutoff: for choose the baseline of the prop in cumsum of the sorted score.
    """
    dirname = os.path.abspath(dirname)
    pick_len = chromoTLPairsNumber(sample_df,os.path.dirname(dirname).replace('Matrix_aligned','SV_result'),cutoff)
    pick_df = sample_df.head(pick_len)
    for chr1,chr2 in zip(pick_df['Chr_i'],pick_df['Chr_j']):
        chr1, chr2 = str(chr1), str(chr2)
        filename = f'{chrname_pre(chr1)}'+chr1+f'_{chrname_pre(chr2)}'+chr2+f'_{num2res_sim(res_unit)}.txt'
        filepath = os.path.join(dirname,filename)
        
        M = sparse_matrix_in(filepath,1,res_unit)
        cutoff = np.percentile(M,99.99,interpolation='nearest') #去掉特别大的值
        M[M>cutoff] = cutoff
        MMT = np.dot(M,M.T)
        MTM = np.dot(M.T,M)
        deDoc_createInputMatrix(MMT,os.path.dirname(dirname),chr1,chr2,f'{num2res_sim(res_unit)}')
        deDoc_createInputMatrix(MTM,os.path.dirname(dirname),chr2,chr1,f'{num2res_sim(res_unit)}')
    return dirname.replace(f"{num2res_sim(res_unit)}",f'square_{num2res_sim(res_unit)}'),pick_len

def deDoc_run(dirname, sample_df, cutoff, deDoc_path,res_unit):
    """
    Input:
        - dirname: ../Matrix_aligned/Sample_name/100k
        - sample_df: chromosome pairs with sorted score
        - cutoff: for choose the baseline of the prop in cumsum of the sorted score.
        - deDoc_path: the path of deDoc.jar
    Return:
        - 
    """
    deDoc_path = os.path.abspath(deDoc_path)
    sq_M_dir,pick_len = deDoc_in_pre(dirname,sample_df,res_unit,cutoff)
    file_L = []
    for filename in os.listdir(sq_M_dir):
        if (filename.find('deDoc')==-1):
            file_L.append(filename)
    for item in file_L:
        print(item)
        if os.path.exists(os.path.join(sq_M_dir,item)+'.deDoc(E).uncontinuedTAD'):
            print("--- continue ---")
            continue
        command = ' '.join(['java','-jar',deDoc_path,os.path.join(sq_M_dir,item)])
        os.system(command)
    return pick_len
        
def breakpoint(MMT):
    """
    Input:
        - MMT: a square matrix for calculating diag-insulation score.
    Return:
        - a score list normalized in [0,1].
    """
    batch_size = np.max([1,np.min([np.int64(MMT.shape[0]/100),10])]) # 1<=batch_size<=10
    left = int(batch_size/2)
    right = batch_size-left
    result = np.zeros((MMT.shape[0],1))
    for lu in range(0,MMT.shape[0]-batch_size+1):
        result[lu+left] = np.mean(MMT[lu:lu+batch_size,lu:lu+batch_size])
    for lu in range(0,left):
        result[lu] = np.mean(MMT[0:lu*2+1,0:lu*2+1])
    for lu in range(MMT.shape[0]-batch_size+1+left,MMT.shape[0]):
        result[lu] = np.mean(MMT[lu-left:,lu-left:])
    return result/np.max(result),batch_size

def TL_section_finder(result,cutline):#rough cut peaks
    """
    Input:
        - result: a numpy list for diag-insulation score.
        - cutline: autofit cutline from other function.
    Return:
        - start: all start point of rough cut region
        - end: all ending point of rough cut region
    """
    seg_cut = 30
    pick = np.where(result>cutline)[0]
    start = [pick[0]]
    end = []
    tmp_index = np.where(np.diff(pick)>seg_cut)[0]
    for i in range(0,len(tmp_index)):
        start.append(pick[tmp_index[i]+1])
        end.append(pick[tmp_index[i]])
    end.append(pick[-1])
    return start,end

def deDocResult(path,name,chr1,chr2,bins):
    """
    Reading the deDoc result.
    Input:
        - path: ../Matrix_aligned
        - name: sample_name
        - chr1,chr2: chromosome pairs
    Return:
        - two point list for enrichment part of high contact.
    """
    res_unit = bins
    filepath = os.path.join(path,name,f'square_{num2res_sim(res_unit)}')
    filename = chr1+"_in_"+chr1+"_"+chr2+".txt.deDoc(E).uncontinuedTAD"
    if (os.path.exists(os.path.join(filepath,filename))):
        f = open(os.path.join(filepath,filename))
    else:
        filename = chr1+"_in_"+chr1+"_"+chr2+".txt.deDoc(M).uncontinuedTAD"
        f = open(os.path.join(filepath,filename))
    high,low = [],[]
    line = f.readline()
    if line.strip()!='':
        high = [int(item)-1 for item in line.strip().split(' ')]
    line = f.readline()
    if line.strip()!='':
        low = [int(item)-1 for item in line.strip().split(' ')]
    return low,high

def auc_cutline(result):
    """
    Input:
        - result: diag-score
    Return:
        - cutline: depends on the area>65% between result and cutline.
    """
    auc_list = []
    step = 0.001
    for cutline in np.arange(step,1,step):
        Sum = sum(result[result>cutline])
        if Sum/sum(result)[0]<0.65:
            break
    return cutline

def TL_section_deDoc(low,high,result):
    """
    Choose the higher part from the deDoc result.
    """
    tmp = []
    if (low == []):
        for i in range(0,len(result)):
            if i not in high:
                low.append(i)
    else:
        for i in range(0,len(result)):
            if (i not in high) and (i not in low):
                tmp.append(i)
    if (np.mean(result[low])>np.mean(result[high])):
        high = low
    if (tmp!=[] and np.mean(result[tmp])>2*np.mean(result[high])):
        high = tmp    
#     print(high)
    return high


def deDoc2Bed(high,chr2,result,cutline,bins):
    df_peak = pd.DataFrame(columns=['chr_id','s','e','Above_95%cut'])
    p = 0
    gap = 3
    df_peak.loc[0]=[f'{chrname_pre(chr2)}'+chr2,high[0]*bins,high[0]*bins,'']

    for i in range(1,len(high)):
        pre = df_peak.loc[p,'e']
        now = high[i]*bins
        if now-pre<=gap*bins:
            df_peak.loc[p,'e'] = now
        else:
            p = p+1
            df_peak.loc[p] = [f'{chrname_pre(chr2)}'+chr2,now,now,'']
    for i in range(len(df_peak)):
        s,e = int(df_peak.loc[i,'s']/bins),int(df_peak.loc[i,'e']/bins)
        if (np.max(result[s:e+1])>cutline):
            df_peak.loc[i,'Above_95%cut'] = 'Yes'
        else:
            df_peak.loc[i,'Above_95%cut'] = 'No'
    return df_peak

def bedcombine(bed,start,end,bins):
    tmpbed = bed.copy(deep=True)
    for p in range(len(tmpbed)):
        s,e = int(tmpbed.loc[p,'s']/bins),int(tmpbed.loc[p,'e']/bins)
        for q in range(len(start)):
            if (s<=start[q] and e<end[q] and e>=start[q]):
                tmpbed.loc[p,'e'] = int(end[q]*bins)
            if (s>start[q] and e<end[q]):
                tmpbed.loc[p,'s'],tmpbed.loc[p,'e'] = int(start[q]*bins),int(end[q]*bins)
            if (s>=start[q] and e>=end[q] and s<=end[q]):
                tmpbed.loc[p,'s'] = int(start[q]*bins)
    result = tmpbed
    p = 0
    for i in range(1,len(tmpbed)):
        s,e = int(result.loc[p,'s']),int(result.loc[p,'e'])
        s_tmp,e_tmp = int(tmpbed.loc[i,'s']),int(tmpbed.loc[i,'e'])
        if (e<s_tmp):
            p = p + 1
            result.loc[p,'s'],result.loc[p,'e'] = s_tmp,e_tmp
        else:
            result.loc[p,'e'] = max(e_tmp,e)
    return result[0:p+1]

def SV_boxfinder(path,name,chr1,chr2,bins):
    """
    Input:
        - path: ../Matrix_align
        - name: sample_name
        - chr1,chr2: chromosome pairs
        - bins: 100k resolution data, 100000
    """
    
#     M = Sparse_in("/media/qian/data_sdb4/projects/Test_out/HiST/Matrix_aligned/"+name+"/100k/chr"+chr1+"_chr"+chr2+"_100k.txt",1)
    matrix_file_path = os.path.join(path,name,f'{num2res_sim(bins)}',f'{chrname_pre(chr1)}'+chr1+f"_{chrname_pre(chr2)}"+chr2+"_100k.txt")
    M = sparse_matrix_in(matrix_file_path, 1)
    cutoff = np.percentile(M,99.99,interpolation='nearest') #去掉特别大的值
    M[M>cutoff] = cutoff
    chr_i = M.shape[0]
    chr_j = M.shape[1]
    
    MMT = np.dot(M,M.T)
    MTM = np.dot(M.T,M)
    result_j,batch_size_j = breakpoint(MTM)
    result_i,batch_size_i = breakpoint(MMT)
#     print('debug!!!!')
    percent_cut = 95
    cutline_i = min(auc_cutline(result_i),np.percentile(result_i,percent_cut))
    cutline_j = min(auc_cutline(result_j),np.percentile(result_j,percent_cut))
    
    ######## 粗略找breakpoint区域 ############
#     percent_cut = 95 #后续要挑breakpoint区域
    start_i,end_i = TL_section_finder(result_i,cutline_i)
    start_j,end_j = TL_section_finder(result_j,cutline_j)
    
    ######## deDoc找TL区域,combine生成最终bed文件 ###########
    low_i,high_i = deDocResult(path,name,chr1,chr2,bins)
    low_j,high_j = deDocResult(path,name,chr2,chr1,bins)
    high_i = TL_section_deDoc(low_i,high_i,result_i)
    high_j = TL_section_deDoc(low_j,high_j,result_j)
    
    Bed_i = deDoc2Bed(high_i,chr1,result_i,cutline_i,bins)
    Bed_j = deDoc2Bed(high_j,chr2,result_j,cutline_j,bins)
    Bed_i_pick = Bed_i[Bed_i['Above_95%cut']=='Yes']
    Bed_j_pick = Bed_j[Bed_j['Above_95%cut']=='Yes']
    Bed_i_pick.reset_index(drop=True,inplace=True)
    Bed_j_pick.reset_index(drop=True,inplace=True)
    result_path = path.replace('Matrix_aligned','SV_result')

    ######## boxmerge ###############
    Bed_com_i = bedcombine(Bed_i_pick,start_i,end_i,bins)
    Bed_com_j = bedcombine(Bed_j_pick,start_j,end_j,bins)
    
    box = pd.DataFrame(columns=['Pairs','chr1','s1','e1','chr2','s2','e2','Box_max','Box_percentile'])
    pairs = chrname_pre(chr1)+chr1+f'_{chrname_pre(chr2)}'+chr2
    i = 0
    for p in range(len(Bed_com_i)):
        for q in range(len(Bed_com_j)):
            if (Bed_com_i.loc[p,'Above_95%cut'] == 'Yes' and Bed_com_j.loc[q,'Above_95%cut'] == 'Yes'):
                sx, sy = int(Bed_com_j.loc[q,'s']),int(Bed_com_i.loc[p,'s'])
                ex, ey = int(Bed_com_j.loc[q,'e']),int(Bed_com_i.loc[p,'e'])
                Box_max = np.max(M[int(sy/bins):int(ey/bins)+1,int(sx/bins):int(ex/bins)+1])
                Box_percetile = np.percentile(M[int(sy/bins):int(ey/bins)+1,int(sx/bins):int(ex/bins)+1],99)
                box.loc[i] = [pairs,chrname_pre(chr1)+chr1,sy,ey,chrname_pre(chr2)+chr2,sx,ex,Box_max,Box_percetile ]
                i = i + 1
    deDocBed = pd.concat([Bed_i_pick,Bed_j_pick],ignore_index=True)
    combineBed = pd.concat([Bed_com_i,Bed_com_j],ignore_index=True)
    return deDocBed,combineBed,box

def PlotBreakpoint(path,name,chr1,chr2,bins):
    """
    Input:
        - path: ../Matrix_align
        - name: sample_name
        - chr1,chr2: chromosome pairs
        - bins: 100k resolution data, 100000
    """
#     M = Sparse_in("/media/qian/data_sdb4/projects/Test_out/HiST/Matrix_aligned/"+name+"/100k/chr"+chr1+"_chr"+chr2+"_100k.txt",1)
    matrix_file_path = os.path.join(path,name,num2res_sim(bins),chrname_pre(chr1)+chr1+f"_{chrname_pre(chr2)}"+chr2+f"_{num2res_sim(bins)}.txt")
    M = sparse_matrix_in(matrix_file_path, 1, bins)
    cutoff = np.percentile(M,99.99,interpolation='nearest') #去掉特别大的值
    M[M>cutoff] = cutoff
    chr_i = M.shape[0]
    chr_j = M.shape[1]
    
    MMT = np.dot(M,M.T)
    MTM = np.dot(M.T,M)
    result_j,batch_size_j = breakpoint(MTM)
    result_i,batch_size_i = breakpoint(MMT)
#     print('debug!!!!')
    percent_cut = 95
#     cutline_i = min(auc_cutline(result_i),np.percentile(result_i,percent_cut))
#     cutline_j = min(auc_cutline(result_j),np.percentile(result_j,percent_cut))
    cutline_i = (auc_cutline(result_i)+np.percentile(result_i,percent_cut))/2.0
    cutline_j = (auc_cutline(result_j)+np.percentile(result_j,percent_cut))/2.0


#     print(cutline_i,cutline_j)
    ######## 粗略找breakpoint区域 ############
    start_i,end_i = TL_section_finder(result_i,cutline_i)
    start_j,end_j = TL_section_finder(result_j,cutline_j)
    
    ######## deDoc找TL区域,combine生成最终bed文件 ###########
    low_i,high_i = deDocResult(path,name,chr1,chr2,bins)
    low_j,high_j = deDocResult(path,name,chr2,chr1,bins)
    high_i = TL_section_deDoc(low_i,high_i,result_i)
    high_j = TL_section_deDoc(low_j,high_j,result_j)
    
    Bed_i = deDoc2Bed(high_i,chr1,result_i,cutline_i,bins)
    Bed_j = deDoc2Bed(high_j,chr2,result_j,cutline_j,bins)
    Bed_i_pick = Bed_i[Bed_i['Above_95%cut']=='Yes']
    Bed_j_pick = Bed_j[Bed_j['Above_95%cut']=='Yes']
    Bed_i_pick.reset_index(drop=True,inplace=True)
    Bed_j_pick.reset_index(drop=True,inplace=True)


    ######## boxmerge ###############
    Bed_com_i = bedcombine(Bed_i_pick,start_i,end_i,bins)
    Bed_com_j = bedcombine(Bed_j_pick,start_j,end_j,bins)
    
    deDocBed = pd.concat([Bed_i_pick,Bed_j_pick],ignore_index=True)
    combineBed = pd.concat([Bed_com_i,Bed_com_j],ignore_index=True)
    box = pd.DataFrame(columns=['Pairs','chr1','s1','e1','chr2','s2','e2','Box_max','Box_percentile'])
    pairs = chrname_pre(chr1)+chr1+f'_{chrname_pre(chr2)}'+chr2
    i = 0
    for p in range(len(Bed_com_i)):
        for q in range(len(Bed_com_j)):
            if (Bed_com_i.loc[p,'Above_95%cut'] == 'Yes' and Bed_com_j.loc[q,'Above_95%cut'] == 'Yes'):
                sx, sy = int(Bed_com_j.loc[q,'s']),int(Bed_com_i.loc[p,'s'])
                ex, ey = int(Bed_com_j.loc[q,'e']),int(Bed_com_i.loc[p,'e'])
                Box_max = np.max(M[int(sy/bins):int(ey/bins)+1,int(sx/bins):int(ex/bins)+1])
                Box_percetile = np.percentile(M[int(sy/bins):int(ey/bins)+1,int(sx/bins):int(ex/bins)+1],99)
                box.loc[i] = [pairs,chrname_pre(chr1)+chr1,sy,ey,chrname_pre(chr2)+chr2,sx,ex,Box_max,Box_percetile ]
                i = i + 1
    
    ######## Plot 染色体对大图准备 ###############
    unit = 0.0035
#     xSize = (chr_j+280)*unit
#     ySize = (chr_i+270)*unit
#     xSize = chr_j*1.2*unit
#     ySize = chr_i*1.25*unit
    xSize = 1500*1.2*unit
    ySize = 1200*1.25*unit    
#     print(chr_i,chr_j)
    plt.close('all')
    fig = plt.figure(figsize=(xSize, ySize))
#     gs = gridspec.GridSpec(3, 2, height_ratios=[200,chr_i,50],width_ratios=[chr_j,200])
    gs = gridspec.GridSpec(3, 2, height_ratios=[20,100,5],width_ratios=[10,2],wspace=0.32, hspace=0.24)
    
    
    ######## Plot chr2 breakpoint 波峰图概览 ##############
    tick_step = 250
    ax0 = plt.subplot(gs[0])
    ax0.plot(result_j)
    ax0.plot(range(0,chr_j),np.ones(chr_j)*cutline_j,'--')
    plt.rcParams['xtick.direction'] = 'in'#将x周的刻度线方向设置向内
    plt.rcParams['ytick.direction'] = 'in'#将y轴的刻度方向设置向内
    plt.xlim([0, chr_j])
    plt.xticks(range(0, chr_j, tick_step))
    ax0.set_xticklabels([])
    plt.yticks([0,0.5,1])

    ######## Plot chr1 breakpoint 波峰图概览 ##############
    ax3 = plt.subplot(gs[3])
    result_i,batch_size_i = breakpoint(MMT)
    ax3.plot(result_i,range(0,len(result_i)))
    ax3.plot(np.ones(chr_i)*cutline_i,range(0,chr_i),'--')
    ax3.set_ylim(bottom=chr_i, top=0)
    ax3.set_xlim(0,1)
    ax3.set_yticklabels([])
    plt.yticks(range(0,chr_i,tick_step))
    plt.xticks([0,0.5,1])
    for tick in ax3.get_xticklabels():
        tick.set_rotation(90)    

    ######## Plot chr1-chr2 交互M heatmap ###############
    ax2 = plt.subplot(gs[2])
    FONTSIZE = 16
    df_heat = df_newheat = pd.DataFrame(M,columns=[f'{i*bins/1e6}M' for i in range(chr_j)],index=[f'{i*bins/1e6}M' for i in range(chr_i)])
    heatplt = sns.heatmap(df_heat, linewidths=0, ax=ax2, cmap="Reds", annot=False, cbar= True, xticklabels=tick_step, yticklabels=tick_step, cbar_ax=plt.subplot(gs[4]),cbar_kws={"orientation": "horizontal"})
    ax2.set_xlabel(chrname_pre(chr2)+chr2,fontsize=FONTSIZE)
    ax2.set_ylabel(chrname_pre(chr1)+chr1,fontsize=FONTSIZE)
#     ax2.tick_params(labelsize=FONTSIZE)
    ax2.xaxis.set_ticks_position('top')
    ax2.yaxis.set_ticks_position('right')
    for tick in ax2.get_xticklabels():
        tick.set_rotation(10)
    for tick in ax2.get_yticklabels():
        tick.set_rotation(360)  
#     fig.tight_layout()
    
    ######## Plot TL deDoc 区域到波峰图 ################   
    ax3.plot(np.zeros(len(high_i)),high_i,'g.')
    ax0.plot(high_j,np.zeros(len(high_j)),'g.')
    
    ######## Plot TL box 区域到热图 ################ 
    sx_min,sy_min = 3000,3000
    ex_max,ey_max = 0,0
    for p in range(len(Bed_com_i)):
        for q in range(len(Bed_com_j)):
            if (Bed_com_i.loc[p,'Above_95%cut'] == 'Yes' and Bed_com_j.loc[q,'Above_95%cut'] == 'Yes'):
                sx, sy = int(Bed_com_j.loc[q,'s']/bins),int(Bed_com_i.loc[p,'s']/bins)
                ex, ey = int(Bed_com_j.loc[q,'e']/bins),int(Bed_com_i.loc[p,'e']/bins)
                rect = patches.Rectangle([sx,sy],ex-sx,ey-sy,ec='g',fill=False)
                ax2.add_patch(rect)
                sx_min = np.min([sx_min,sx])
                sy_min = np.min([sy_min,sy])
                ex_max = np.max([ex_max,ex])
                ey_max = np.max([ey_max,ey])
    box_percentile_cut = np.max(box['Box_percentile'])/2
    for i in box.index:
        if box.loc[i,'Box_percentile']>box_percentile_cut:
            sx,ex,sy,ey = box.loc[i,'s2'],box.loc[i,'e2'],box.loc[i,'s1'],box.loc[i,'e1']
            rect = patches.Rectangle([int(sx/bins),int(sy/bins)],int(ex/bins)-int(sx/bins),int(ey/bins)-int(sy/bins),ec='r',fill=False)
            ax2.add_patch(rect)
    sx = np.max([0,sx_min-50])
    ex = np.min([ex_max+50,chr_j])
    sy = np.max([0,sy_min-50])
    ey = np.min([ey_max+50,chr_i])
    rect = patches.Rectangle([sx,sy],ex-sx,ey-sy,lw=0.5,ls='--',ec='gray',fill=False)
    ax2.add_patch(rect)

    ######## Plot TL box zoom in ################ 
    xSize2 = 5*unit*(ex-sx)
    ySize2 = 5*unit*(ey-sy)
    if (xSize2>0 and ySize2>0):
        fig2 = plt.figure(figsize=(xSize2,ySize2))
        ax_newheat = fig2.add_subplot(1,1,1)  
        df_newheat = pd.DataFrame(M[sy:ey,sx:ex],columns=[f'{i*bins/1e6}M' for i in range(sx,ex)],index=[f'{i*bins/1e6}M' for i in range(sy,ey)])
        heatplt_2 = sns.heatmap(df_newheat, linewidths=0, ax=ax_newheat, cmap="Reds", annot=False, cbar= False, xticklabels=50, yticklabels=20)
        ax_newheat.tick_params(labelsize=18)
        ax_newheat.set_xlabel(chrname_pre(chr2)+chr2)
        ax_newheat.set_ylabel(chrname_pre(chr1)+chr1)
        sx_zoom,sy_zoom,ex_zoom,ey_zoom = sx,sy,ex,ey
        for p in range(len(Bed_com_i)):
            for q in range(len(Bed_com_j)):
                if (Bed_com_i.loc[p,'Above_95%cut'] == 'Yes' and Bed_com_j.loc[q,'Above_95%cut'] == 'Yes'):
                    sx, sy = int(Bed_com_j.loc[q,'s']/bins),int(Bed_com_i.loc[p,'s']/bins)
                    ex, ey = int(Bed_com_j.loc[q,'e']/bins),int(Bed_com_i.loc[p,'e']/bins)
                    rect = patches.Rectangle([sx-sx_zoom,sy-sy_zoom],ex-sx,ey-sy,ec='g',fill=False)
                    ax_newheat.add_patch(rect)

        fig2.tight_layout()
#     return deDocBed,combineBed,box,fig,fig2
    return deDocBed,combineBed,box,fig
    
def TLplotandBEDproduce(path,name,dataset,res_unit,no_pic_fg=False):
    deDocBed_all = pd.DataFrame()
    combineBed_all = pd.DataFrame()
    box_all = pd.DataFrame()
    box_filter = pd.DataFrame()
    print(name,' SV chromosome pairs:',len(dataset))
    result_path = path.replace('Matrix_aligned','SV_result')
    for i in dataset.index:
        chr1,chr2 = str(dataset.loc[i,'Chr_i']),str(dataset.loc[i,'Chr_j'])
        print(i,chr1,chr2)
        if not no_pic_fg:
#             deDocBed,combineBed,box,fig,fig2 = PlotBreakpoint(path,name,chr1,chr2)
            deDocBed,combineBed,box,fig = PlotBreakpoint(path,name,chr1,chr2,res_unit)
            fig_path = os.path.join(result_path,name,'pic')
            if not os.path.exists(fig_path):
                os.makedirs(fig_path)
                print(f'------- Create new pic path in folder {fig_path} ---')
            fig.savefig(os.path.join(fig_path,str(i)+f'_Combine_{chrname_pre(chr1)}'+chr1+f'_{chrname_pre(chr2)}'+chr2+'.png'),dpi=400,format='png')
#             fig2.savefig(os.path.join(fig_path,str(i)+'_Combine_chr'+chr1+'_chr'+chr2+'_zoomin.png'),dpi=400,format='png')
        else:
            deDocBed,combineBed,box=SV_boxfinder(path,name,chr1,chr2,res_unit)
        deDocBed_all = pd.concat([deDocBed_all,deDocBed],ignore_index=True)
        combineBed_all = pd.concat([combineBed_all,combineBed],ignore_index=True)
        box_all = pd.concat([box_all,box],ignore_index=True)
        if len(box)<=10:
            box_filter = pd.concat([box_filter,box],ignore_index=True)
        else:
            box_filter_cut = np.max(box['Box_percentile'])/2
            box_tmp = box[box.Box_percentile>box_filter_cut]
            if len(box_tmp)<=18:
                box_filter = pd.concat([box_filter,box_tmp],ignore_index=True)
           
    
    deDocBed_all.to_csv(os.path.join(result_path,name,'SV_deDocBed_all.csv'),index=False)
    combineBed_all.to_csv(os.path.join(result_path,name,'SV_combineBed_all.csv'),index=False)
    box_all.to_csv(os.path.join(result_path,name,'SV_box_all.csv'),index=False)
    box_filter.to_csv(os.path.join(result_path,name,'SV_box_filtered.csv'),index=False)
    
        
if __name__ == "__main__":
#     path = '/media/qian/data_sdb4/projects/HiC_SV/HiC_translocation_test/Test/HiST_0.2_demo/Matrix_aligned/Test_GSE63525_K562_combined_30/100k'
#     deDoc_path = '/home/qian/software/deDoc/deDoc.jar'
    
#     deDoc_matrix_in_path = deDoc_in_pre(path,Rao_K562_sort,0.1)
#     deDoc_run(deDoc_path, deDoc_matrix_in_path)
    
#     path = '/media/qian/data_sdb4/projects/HiC_SV/HiC_translocation_test/Test/HiST_0.2_demo/Matrix_aligned'
    deDoc_path = '/home/qian/software/deDoc/deDoc.jar'
#     sv_result_path = "/media/qian/data_sdb4/projects/HiC_SV/HiC_translocation_test/Test/HiST_0.2_demo/SV_result"
#     name_K562 = 'Test_GSE63525_K562_combined_30'
#     Rao_K562_sort = pd.read_csv("../Test/HiST_0.2_demo/SV_result/Test_GSE63525_K562_combined_30/Test_GSE63525_K562_combined_30_result_500k_sorted.csv")
    
    path = '/media/qian/data_sdb4/projects/Test_out/HiST/Matrix_aligned/'
    sv_result_path = '/media/qian/data_sdb4/projects/Test_out/HiST/SV_result/'
#     name_caki2 = 'Test_Dekker_Caki2'
#     Dekker_caki2_sort = pd.read_csv("/media/qian/data_sdb4/projects/Test_out/HiST/SV_result/Test_Dekker_Caki2/Test_Dekker_Caki2_result_500k_sorted.csv")
    
#     result_pick_len = deDoc_run(os.path.join(path,name_K562,'100k'), Rao_K562_sort, 0.4, deDoc_path)
#     TLplotandBEDproduce(path,name_K562,Rao_K562_sort[0:result_pick_len])
#     df_peak_K562 = TLplotandBEDproduce(path,name_K562,Rao_K562_sort[0:result_pick_len])
#     result_pick_len = deDoc_run(os.path.join(path,name_caki2,'100k'), Dekker_caki2_sort, 0.4, deDoc_path)
#     TLplotandBEDproduce(path,name_caki2,Dekker_caki2_sort[0:3])
#     Li_U266_sort = pd.read_csv("/media/qian/data_sdb4/projects/Test_out/HiST/SV_result/Li_U266_HindIII/Li_U266_HindIII_result_500k_sorted.csv")
#     name_U266 = 'Li_U266_HindIII'
#     TLplotandBEDproduce(path,name_U266,Li_U266_sort[14:15])
    
#     path = '/media/qian/data_sdd/work_dir/TL_output/Matrix_aligned/'
#     sv_result_path = '/media/qian/data_sdd/work_dir/TL_output/SV_result/'
    
#     BRD3179_sort = pd.read_csv("/media/qian/data_sdd/work_dir/TL_output/SV_result/Test_GSM3930259_BRD3179/Test_GSM3930259_BRD3179_result_500k_sorted.csv")
#     name_BRD3179 = 'Test_GSM3930259_BRD3179'
#     TLplotandBEDproduce(path,name_BRD3179,BRD3179_sort[0:10])

    Dekker_Panc1_sort = pd.read_csv("/media/qian/data_sdb4/projects/Test_out/HiST/SV_result/Dekker_Panc1A/Dekker_Panc1A_result_500k_sorted.csv")
    name_panc1 = 'Dekker_Panc1A'
    TLplotandBEDproduce(path,name_panc1,Dekker_Panc1_sort[0:43])
                                       