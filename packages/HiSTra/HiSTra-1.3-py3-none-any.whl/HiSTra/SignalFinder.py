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

from HiSTra.utils import *
from HiSTra.SparseMatrixDeal import sparse_matrix_in

def Eigen_calculation(path_in,k,sizes): 
    """Calculate the eigenvalue list of all chromosome pairs of a sample.
    Input:
        - path_in, the dirpath like ../matrix_aligned/sample_name/.
        - k, resolution index of ["500k/","100k/"], 0->500k, 1->100k.
    Return:
        - evalue_file_path, the abspath of a file, which is a numpy.array((253,500or2500)).
    """
    path_in = os.path.abspath(path_in)
    chrname = sizes2chrname(sizes)
    res_unit = sizes2resUnit(sizes)
    res_low = res_unit*5
    res_high = res_unit
    
    interchr_num = int(len(chrname)*(len(chrname)-1)/2)
    max_chrlen_list = [int(sizes.max()[1]/5/res_unit)+10,int(sizes.max()[1]/res_unit)+10]
    max_chrlen = max_chrlen_list[k]
    eigen_value_L = np.zeros((interchr_num,max_chrlen),dtype=float,order='C')

    files_full = sparsefiles(k,sizes) # all files in dir ../matrix_aligned/sample_name/*00k/
    files = []
    for filename in files_full:
        if not intra(filename):
            files.append(filename)
    
    resolution = [f"{num2res_sim(res_low)}",f"{num2res_sim(res_high)}"]
    for p,filename in enumerate(files): # filename format is *00k/chr1_chr2_*.txt
        M = sparse_matrix_in(os.path.join(path_in,filename), k, res_unit) # float 乘法快！但是转化很慢。
        cutoff = np.percentile(M,99.99,interpolation='nearest') #去掉特别大的值
        M[M>cutoff] = cutoff
        MMT = np.dot(M,M.T)
        MTM = np.dot(M.T,M)
        eigenvalue,eigenvector = np.linalg.eigh(MMT,UPLO='L')
        eigen_value_L[p,:]=np.pad(eigenvalue,(0,max_chrlen-len(eigenvalue)),'constant',constant_values=np.nan)
        
        chr1,chr2 = os.path.basename(filename).split('_')[0],os.path.basename(filename).split('_')[1]
#         deDoc_createInputMatrix(MMT,path_in,chr1,chr2,resolution[k])
#         deDoc_createInputMatrix(MTM,path_in,chr2,chr1,resolution[k])

    path_out = path_in.replace("Matrix_aligned","Eigen")
    sample_name = os.path.basename(path_out)    
    
    if not os.path.exists(path_out):
        os.makedirs(path_out)
        print(f"------ Create Eigen folder for {sample_name}... ---")
    else:
        print(f"------ Corresponding Eigen folder of {sample_name} exists. ---")
    evalue_file_path = os.path.join(path_out,'_'.join([sample_name,resolution[k],"evalue.npy"]))
    np.save(evalue_file_path,eigen_value_L)
        
    print(f"------ We have finished {len(files)} pairs of interchromosomes in resolution {resolution[k]}. ------")
    return eigen_value_L,evalue_file_path

def Outlier(eigenvalue):
    """Count the number of outliers of an eigenvalue list using histogram. Autochoose the hist bin.
    Two super-parameters: 
        resolution_hist, 88%percentile; 
        Outlier definition, [98,76,4,0,0,...,1,0,0,...,1], choose [4,0,0,...,1,0,0,...,1].
    """
    z = eigenvalue
    number_Max = len(z[z>1e7])#特别大的离值点单独统计 防止bins过多影响效率
    z = z[z<=1e7]
    resolution_hist=np.percentile(z,88,interpolation='nearest')
    number_bin = np.maximum(np.int64(np.amax(z)/resolution_hist),1)
    H,bin_edges = np.histogram(z,bins=number_bin)
    p = -1
    h = H[p:]
    while len(H[H==0])>len(h[h==0]) and np.amax(h)<=2:
        p = p - 1
        h = H[p:]
    while (len(H)>2-p and H[p-1]<5):
        p = p - 1
        h = H[p:]
    if (len(H)==1 or h[0]>=5):
        return 0
    return sum(h)+number_Max  
    
def compare_evalue(test_evalue,control_evalue,chrname):
    """Calculate the SV score between two eigenvalue lists.
    Input: eigenvalue list of test sample and control sample.
    Output: number of outliers, difference, pearson correlation expect outliers.
        Final colunm is the SV score.
    """
    # 输入均为二维数组 内含np.nan数字补齐 后续考虑没有control的情况！！！
    # 平行比较test和control同一对chromosomes的特征值相关性，差异大的认为大概率存在变异
    # 此函数单纯输出线性相关性
    correlation_L = []
    if (test_evalue.shape!=control_evalue.shape):
        print('Error! Different shape between eigenvalue of test and control!')
    eigen_pair_list = []
    for chri,chrj in itertools.combinations(chrname,2):
        eigen_pair_list.append('--'.join([chri,chrj]))
        
    for k in range(test_evalue.shape[0]):
        eigen_c = abs(test_evalue[k,:])[abs(test_evalue[k,:])>0.1]
        eigen_n = abs(control_evalue[k,:])[abs(control_evalue[k,:])>0.1]
        eigen_c_log = np.log(abs(test_evalue[k,:])[abs(test_evalue[k,:])>0.1])
        eigen_n_log = np.log(abs(control_evalue[k,:])[abs(control_evalue[k,:])>0.1])
        
        Outlier_test = Outlier(eigen_c)
        Outlier_control = Outlier(eigen_n)
        
        end_test = len(eigen_c_log)-Outlier_test
        end_control = len(eigen_n_log)-Outlier_control
        Len_pick = max(min(end_test-len(eigen_c[eigen_c<10]), # choose at least 5 items, this part is exclude
                       end_control-len(eigen_n[eigen_n<10]))-10,5) # outliers and the start points.
        chr_i,chr_j = eigen_pos2chr_pos(k,eigen_pair_list)
        
        r,p = st.pearsonr(eigen_c_log[end_test-Len_pick:end_test],eigen_n_log[end_control-Len_pick:end_control])
        # chr_i,chr_j = eigen_pos2chr_pos(k)        
        correlation_L.append([chr_i,chr_j,r,p,
                              np.mean(eigen_c_log[-1:]), np.mean(eigen_n_log[-1:]),
                              np.mean(eigen_c_log[-1:])-np.mean(eigen_n_log[-1:]),
                              Outlier_test,Outlier_control,Outlier_test-Outlier_control,
                             Outlier_test-Outlier_control+np.mean(eigen_c_log[-1:])-np.mean(eigen_n_log[-1:])])
    column_name = ["Chr_i","Chr_j","Correlation","P_value",
                   "AveEvalue_test","AveEvalue_control",
                   "AveEvalue_difference",
                   "Outlier_test","Outlier_control","Outlier_difference",
                   "Score"]
    correlation_df = pd.DataFrame(columns = column_name, data = correlation_L)
    return correlation_df      

def evalue2TLpairs(result_path,test_sample_name,test_500k_evalue,control_500k_evalue,sizes):# for single sample, which means in the path should be contained only one npzfile of each resolution of the expected sample.
    """Detect the chromosome pair in which TL occur.
    Input:
        - result_path, the output saving dirpath. User set it.
        - test_sample_name, for saving result.
        - test_evalue/control_evalue, the eigenvalue list of test/control.
    Output:
        - result_path. The chromosome pairs are save in ../SV_result/test_sample_name/
    """ 
    chrname = sizes2chrname(sizes)
    res_unit = sizes2resUnit(sizes)
    # compare相关性获得
    chr_pair_500k_df = compare_evalue(test_500k_evalue,control_500k_evalue,chrname) #获得单纯的相关性
    
    # compare结果排序and过滤
    chr_pair_500k_df_sort = chr_pair_500k_df.sort_values(by= ["Score","Outlier_difference","Correlation","AveEvalue_difference","Chr_i","Chr_j"],ascending = [False,False,True,False,True,True])
    chr_pair_500k_df_sort.reset_index(drop=True,inplace=True) # 扔掉过滤前的旧index
    
    # 过滤后的结果全部输出保存
    result_path = os.path.abspath(result_path)
    result_path = os.path.join(result_path,"SV_result", test_sample_name)
    folder = os.path.exists(result_path)
    if not folder:
        os.makedirs(result_path)
        print("------ Create new SV_result folder... ------")
    else:
        print("------ Corresponding SV_result folder exists. ------")
    chr_pair_500k_df.to_csv(os.path.join(result_path,test_sample_name+f"_result_{num2res_sim(res_unit*5)}.csv"),index=False)
    chr_pair_500k_df_sort.to_csv(os.path.join(result_path,test_sample_name+f"_result_{num2res_sim(res_unit*5)}_sorted.csv"),index=False)
    return result_path


def signalFinder(result_path,test_matrix_path,control_matrix_path,sizes):
    """Function which will be linked to main run script.
    Input user_set result path, and matrix_aligned/test_sample(control_sample),
    Return SV_result path like ../SV_result/test_sample_name/
    """
    evalue_500k_test,evalue_500k_filepath_test = Eigen_calculation(test_matrix_path,0,sizes)
    evalue_500k_control,evalue_500k_filepath_control = Eigen_calculation(control_matrix_path,0,sizes)
    test_sample_name = os.path.basename(test_matrix_path)
    SV_resultpath = evalue2TLpairs(result_path,test_sample_name,evalue_500k_test,evalue_500k_control,sizes)
    return SV_resultpath
    
if __name__ == "__main__":
    test_matrix_path = "/media/qian/data_sdb4/projects/HiC_SV/HiC_translocation_test/Test/HiST_0.2_demo/Matrix_aligned/GSE63525_K562_combined_30"
    control_matrix_path = "/media/qian/data_sdb4/projects/HiC_SV/HiC_translocation_test/Test/HiST_0.2_demo/Matrix_aligned/GSE63525_IMR90_combined_30_downsample_for_GSE63525_K562_combined_30"
    result_path = "/media/qian/data_sdb4/projects/HiC_SV/HiC_translocation_test/Test/HiST_0.2_demo"
    SV_resultpath = signalFinder(result_path,test_matrix_path,control_matrix_path)
    print(SV_resultpath)
    
# # path 是单样本的路径
# if __name__ == "__main__":
#     wd = "/media/qian/data_sdb4/projects/HiC_SV/HiC_translocation_test/Test/HiST_0.2_demo/Matrix_aligned/"
#     dirs = os.listdir(wd)
#     dirs = ["GSE63525_K562_combined_30","GSE63525_IMR90_combined_30_downsample_for_GSE63525_K562_combined_30"]
#     for dir_name in dirs:
#         path = os.path.join(wd,dir_name)
#         print(path)
# #     path = "/media/qian/data_sdb4/projects/HiC_SV/HiC_translocation_test/Test/HiST_0.2_demo/Matrix_from_hic/GSE63525_GM12878_insitu_primary_30/" 
#         start = datetime.now()
#         print(f"--- START TIME is: {start} ---")
#         evalue_500k,evalue_500k_filepath = Eigen_calculation(path,0)
#         end = datetime.now()
#         print(f"--- Complete resolution 500k at {end} ---")
#         print(f"--- --- Consuming time is: {end-start} --- ---")
#         print(f"--- The eigenvalue filepath is {evalue_500k_filepath} ---")
#         start = datetime.now()
#         print(f"--- START TIME is: {start} ---")
#         evalue_100k,evalue_100k_filepath = Eigen_calculation(path,1)
#         end = datetime.now()
#         print(f"--- Complete resolution 100k at {end} ---")
#         print(f"--- --- Consuming time is: {end-start} --- ---")
#         print(f"--- The eigenvalue filepath is {evalue_100k_filepath} ---")
    
def deDoc_createInputMatrix(MMT,dirname,chr1,chr2,resolution):
    """Save covariance matrix as deDoc input files.
    Input:
        - MMT, covariance matrix.
        - dirname, ../matrix_aligned/sample_name
        - chr1, chr2, the chromosome pairs.
        - resolution, determine the savepath is dirname/square_*00k/chr1_in_chr1_chr2.txt
    Return:
        None.
    """
    X1 = sparse.coo_matrix(MMT)
    col =np.int64( X1.col + 1)
    row = np.int64(X1.row + 1)
    data = X1.data
    X1 = np.array([col,row,data]).T
    
    deDoc_in_dir = os.path.join(dirname,'_'.join(["square",resolution]))
    folder = os.path.exists(deDoc_in_dir)
    if not folder:
        os.makedirs(deDoc_in_dir)
        print(f"--- Create new deDoc folder in {deDoc_in_dir}... ---")

    np.savetxt(os.path.join(deDoc_in_dir, chr1+'_in_'+chr1+'_'+chr2+'.txt'),X1,fmt='%d %d %.1lf',header=str(len(X1.data)),comments='')