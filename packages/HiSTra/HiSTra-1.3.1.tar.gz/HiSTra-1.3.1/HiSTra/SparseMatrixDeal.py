#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" All functions are used for reading, downsample raw matrices, and save downsampled Sparse Matrices.

Available functions:
- linkmatrix: Make a soft link from matrix_from_hic to Matrix_aligned, for the matrix files which are not downsampled.
- sparse_matrix_in: Load a single matrix file, normally it is a txt within 3 columns without header, which are (pos_i,pos_j,counts).
- downsample: Align the depth of test sample and control sample.
- downsampleSaveas: For each matrix files, do the downsample and save the downsampled file in new dir.

"""
import sys
import getopt
import os
import fnmatch
import random
import numpy as np
import pandas as pd
import itertools
from datetime import *
from scipy import sparse
from random import sample

from HiSTra.utils import sparsefiles,intra

def linkmatrix(path): 
    """Make a soft link from matrix_from_hic to Matrix_aligned, for the matrix files which are not downsampled."""
    sourcefile = os.path.abspath(path)
    link_path = os.path.dirname(sourcefile).replace("Matrix_from_hic","Matrix_aligned")
    destfile = sourcefile.replace("Matrix_from_hic","Matrix_aligned")
    command = "ln -s " + sourcefile +' '+ destfile
    if not os.path.exists(link_path):
        os.makedirs(link_path)
        print("---- Create new matrix_aligned folder... ----")
    else:
        print("---- The matrix_aligned folder has existed... ----")
    if not os.path.exists(destfile):
        os.system(command)

def sparse_matrix_in(matrix_file,k,res_unit): #pandas 读入单个chri_chrj_100k.txt/chri_chrj_500k.txt的函数块 输出一个np.array数组便于计算
    """Load a single matrix file, normally it is a txt within 3 columns without header, which are (pos_i,pos_j,counts).
        matrix_file: abspath of ../Matrix_from_hic/A_sample/*00k/chri_chrj_*00k.txt
        k: for resolution, 0 is 500k, 1 is 100k.
        res_unit:the resolution adapted for the chromosome, e.g human 100k, yeast 1k.
    Return the corresponding numpy.array for calculation.
    """
    # file是sparse matrix完整路径名字
    # k是分辨率编号
    data = pd.read_csv(matrix_file,header=None,sep='\t')
    res_value = [5*res_unit,res_unit]
    row = np.int64(data[0]/res_value[k])
    column = np.int64(data[1]/res_value[k])
    weight = np.float64(data[2])
    sp = sparse.coo_matrix((weight,(row,column)))
    return sp.toarray()

def downsample(test_path,control_path,k,sizes): #pandas 读入单个chri_chrj_100k.txt/chri_chrj_500k.txt的函数块 输出一个np.array数组便于计算
    """Load path of test and control sample and align their depth, create a new dir named Matrix_aligned. 
        test_path: ../matrix_from_hic/test_sample
        control_path: ../matrix_from_hic/control_sample
    Return depth ratio and new paths, content in () sometimes is not necessary.
        testDir_mat_aligned: ../matrix_aligned/test_sample(_downsample_for_control_sample)
        controlDir_mat_aligned: ../matrix_aligned/control_sample(_downsample_for_test_sample)
    """
    # *_path是绝对路径
    # k是分辨率编号
    test_path = os.path.abspath(test_path)
    control_path = os.path.abspath(control_path)
    files = sparsefiles(k,sizes)
    test_depth = 0
    control_depth = 0
    for filename in files:
        # print(filename)
        test_M = pd.read_csv(os.path.join(test_path,filename),header=None,sep='\t')
        control_M = pd.read_csv(os.path.join(control_path,filename),header=None,sep='\t')
        test_depth += (sum(test_M[2]))
        control_depth += (sum(control_M[2]))
#     result = pd.DataFrame((test_depth,control_depth))
    
    testDir_mat_aligned = test_path.replace("Matrix_from_hic","Matrix_aligned")
    controlDir_mat_aligned = control_path.replace("Matrix_from_hic","Matrix_aligned")
    
    if test_depth<control_depth:
        ratio = test_depth/control_depth
        linkmatrix(test_path)
        
        if ratio<0.9:
            for filename in files:
                if not intra(filename):
                    # print(filename) # for debug
                    downsampleSaveas(control_path,filename,ratio,os.path.basename(test_path))
            controlDir_mat_aligned = ''.join([control_path.replace("Matrix_from_hic","Matrix_aligned")
                                              ,"_downsample_for_",os.path.basename(test_path)])
        else:
            linkmatrix(control_path)
    else:
        ratio = control_depth/test_depth
        linkmatrix(control_path)
        if ratio<0.9:
            for filename in files:
                if not intra(filename):
                    # print(filename) # for debug
                    downsampleSaveas(test_path,filename,ratio,os.path.basename(control_path))
            testDir_mat_aligned = ''.join([test_path.replace("Matrix_from_hic","Matrix_aligned")
                                           ,"_downsample_for_", os.path.basename(control_path)])
        else:
            linkmatrix(test_path)
            
    return ratio,testDir_mat_aligned,controlDir_mat_aligned

def downsampleSaveas(path,file,ratio,test_name): # 注意 file的格式是500k/***.txt,100k/***.txt
    """Core part of downsample.
    Load the matrix file which will be downsampled, the ratio of downsampling, the output file name.
        path: ../matrix_from_hic/A_sample
        file: *00k/chri_chrj_*00k.txt
        test_name: the sample_name
    No return.
    """
    path = os.path.abspath(path)
    path_tosave = path.replace("Matrix_from_hic","Matrix_aligned") + "_downsample_for_" + test_name
    if not os.path.exists(os.path.join(path_tosave,file)):
        df = pd.read_csv(os.path.join(path,file),header=None,sep='\t')
        df.columns=['x','y','w']
        df_result = df.sample(n=np.int64(sum(df['w'])*ratio),weights=df['w'],replace=True,random_state=1)

        df_downsample = pd.DataFrame(df_result[['x','y']].value_counts(sort=False),dtype=float)
        depth_down = df_downsample.reset_index().rename(columns={0:'w'})


        if not os.path.exists(os.path.dirname(os.path.join(path_tosave,file))): # create ../Matrix_aligned/*00k
            os.makedirs(os.path.dirname(os.path.join(path_tosave,file)))
        depth_down.to_csv(os.path.join(path_tosave,file),header=None,sep='\t',index=None)
        print(f"------Create. Aligned matrix is {file}.")
    else:
        print(f"------Reanalyse.{file} exists. Continue.")
     

if __name__ == "__main__":
    test_path = "/media/qian/data_sdb4/projects/HiC_SV/HiC_translocation_test/Test/HiST_0.2_demo/Matrix_from_hic/Dekker_Caki2_HiC"
    control_path = "/media/qian/data_sdb4/projects/HiC_SV/HiC_translocation_test/Test/HiST_0.2_demo/Matrix_from_hic/GSE63525_IMR90_combined_30"
    start = datetime.now()
    ratio500k,testDir_mat_aligned,controlDir_mat_aligned = downsample(test_path,control_path,0)
    ratio100k,testDir_mat_aligned,controlDir_mat_aligned = downsample(test_path,control_path,1)
    end = datetime.now()
    print("--- Debug Test: Depth difference is big: \n",ratio500k,ratio100k)
    print(f"--- --- Consuming time is: {end-start} --- ---")
    test_path = "/media/qian/data_sdb4/projects/HiC_SV/HiC_translocation_test/Test/HiST_0.2_demo/Matrix_from_hic/GSE63525_K562_combined_30"
    control_path = "/media/qian/data_sdb4/projects/HiC_SV/HiC_translocation_test/Test/HiST_0.2_demo/Matrix_from_hic/GSE63525_IMR90_combined_30"
    start = datetime.now()
    ratio500k,testDir_mat_aligned,controlDir_mat_aligned = downsample(test_path,control_path,0)
    ratio100k,testDir_mat_aligned,controlDir_mat_aligned = downsample(test_path,control_path,1)
    end = datetime.now()
    print("--- Debug Test: Depth difference is small: \n",ratio500k,ratio100k)
    print(f"--- --- Consuming time is: {end-start} --- ---")
    
