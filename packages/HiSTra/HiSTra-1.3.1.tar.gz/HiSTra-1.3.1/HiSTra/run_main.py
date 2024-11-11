#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import getopt
import os
import fnmatch
import itertools

import numpy as np
import pandas as pd
import scipy.stats as st
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import seaborn as sns

from datetime import *
from scipy import sparse

from HiSTra.utils import *
from HiSTra.hicInput import hic2mat,cool2mat
from HiSTra.SparseMatrixDeal import *
from HiSTra.SignalFinder import *
from HiSTra.BoxFinder import *


def precheck(prog_args):
    test_path=os.path.abspath(os.path.expanduser(prog_args.test))
    control_path=os.path.abspath(os.path.expanduser(prog_args.control))
    sizes_path=os.path.abspath(os.path.expanduser(prog_args.sizes))
    output_path=os.path.abspath(os.path.expanduser(prog_args.output))
    juice_path=os.path.abspath(os.path.expanduser(prog_args.juice))
    deDoc_path=os.path.abspath(os.path.expanduser(prog_args.deDoc))
#     print(prog_args.baseline)
#     print(prog_args.no_figure)
    if (not os.path.exists(juice_path)) or ('.jar' not in juice_path):
        if (test_path.endswith('.hic') or control_path.endswith('.hic')):
            print('juice_path is set: ',juice_path)
            print("-------Error! Juicer tools are not found.---------")
            return False
    if (not os.path.exists(deDoc_path)) or ('.jar' not in deDoc_path):
        print('deDoc_path is set: ',deDoc_path)
        print("-------Error! deDoc.jar are not found.---------")
        return False
    if (not os.path.exists(test_path)) or (not (test_path.endswith('.hic') or test_path.endswith('.mcool'))):
        print('test_path is set: ',test_path)
        print("-------Error! Test sample hicfile/coolfile are not found.---------")
        return False
    if (not os.path.exists(control_path)) or (not(control_path.endswith('.hic') or control_path.endswith('.mcool'))):
        print('control_path is set: ',control_path)
        print("-------Error! Control sample hicfile/coolfile are not found.---------")
        return False
    if (not os.path.exists(sizes_path)):
        print('sizes_path is set: ',sizes_path)
        print("-------Error! Chromosome sizes are not found.---------")
        return False
    return True

def run_main(prog_args):
    start = datetime.now()
    #------ Precheck --------
    if not precheck(prog_args):
        sys.exit()
    else:
        test_path=os.path.abspath(os.path.expanduser(prog_args.test))
        sizes_path=os.path.abspath(os.path.expanduser(prog_args.sizes))
        control_path=os.path.abspath(os.path.expanduser(prog_args.control))
        output_path=os.path.abspath(os.path.expanduser(prog_args.output))
        if (test_path.endswith('.hic') or control_path.endswith('.hic')):
            juice_path=os.path.abspath(os.path.expanduser(prog_args.juice))
        deDoc_path=os.path.abspath(os.path.expanduser(prog_args.deDoc))
        sizes = pd.read_csv(sizes_path,sep='\t',header=None) # feature-yeast, add sizes file, which is required.
        if (test_path.endswith('.hic') or control_path.endswith('.hic')):
            print('juice_path is set: ',juice_path)
        print('deDoc_path is set: ',deDoc_path)
        print('output_path is set: ',output_path)
        print(f"------- Precheck Work finish. -------")
    # ------ Step 1 Dump matrix. -------
    if test_path.endswith('.hic'):
        testDir_Mat_from_hic = hic2mat(test_path,output_path,juice_path,sizes)
    if test_path.endswith('.mcool'):
        testDir_Mat_from_hic = cool2mat(test_path,output_path,sizes)
    if control_path.endswith('.hic'):
        controlDir_Mat_from_hic = hic2mat(control_path,output_path,juice_path,sizes)
    if control_path.endswith('.mcool'):
        controlDir_Mat_from_hic = cool2mat(control_path,output_path,sizes)
    # ----- time consumed print -------
    end1 = datetime.now()
    print(f"------ Your test sample hicfile is dumpped in {testDir_Mat_from_hic}. ------")
    print(f"------ Your control sample hicfile is dumpped in {controlDir_Mat_from_hic}. ------")
    print(f"--- Step 1 hic2matrix finish. Consuming {end1-start}. --- \n")
    
    #------- Step2 Align matrix depth. ------
    ratio500k,testDir_mat_aligned,controlDir_mat_aligned = downsample(testDir_Mat_from_hic,controlDir_Mat_from_hic,0,sizes)
    ratio100k,testDir_mat_aligned,controlDir_mat_aligned = downsample(testDir_Mat_from_hic,controlDir_Mat_from_hic,1,sizes)
    # ----- time consumed print -------
    end2 = datetime.now()
    print(f"------ The matrices are aligen in {testDir_mat_aligned} and {controlDir_mat_aligned}. ------ ")# for debug
    print(f"--- Step 2 finish. Matrices are aligned. Consuming {end2-end1} ---\n")    
    
    # ------- Step3 SV signal finder -----
    SV_resultpath = signalFinder(output_path,testDir_mat_aligned,controlDir_mat_aligned,sizes)
    # ----- time consumed print -------
    end3 = datetime.now()
    print(f"------ Translocation score is saved in {SV_resultpath}")
    print(f"--- Step 3 finish. Raw translocation score are sorted. Consuming {end3-end2}. ---\n")
    
    # ------- Step4 SV box finder -----
    res_unit = sizes2resUnit(sizes)
    for file in os.listdir(SV_resultpath):
        if fnmatch.fnmatch(file,'*sorted.csv'):
            sv_result_sort = pd.read_csv(os.path.join(SV_resultpath,file))
    result_pick_len = deDoc_run(os.path.join(testDir_mat_aligned,num2res_sim(res_unit)), sv_result_sort, prog_args.baseline, deDoc_path, res_unit)
    path = os.path.dirname(testDir_mat_aligned)
    sample_name = os.path.basename(testDir_mat_aligned)
    if not (prog_args.top==0):
#         result_pick_len = min(result_pick_len,prog_args.top) #edit log 2021-11-17 to extend the --top parameter
        result_pick_len = prog_args.top
    TLplotandBEDproduce(path,sample_name,sv_result_sort[0:result_pick_len],res_unit,prog_args.no_figure)
    # ----- time consumed print -------
    end4 = datetime.now()
    print(f"------ Translocation boxes are saved in {SV_resultpath}")
    print(f"--- Step 4 finish. Translocation boxes are listed. Consuming {end4-end3}. ---")
    
if __name__=="__main__":
    print('test!!')
#     test_path,control_path,output_path,juice_path,deDoc_path=path_get()
#     if juice_path == "":
#         juice_path = "/home/qian/software/juicer_tools_1.22.01.jar"
#         print("-------Error! Juicer tools are not found.---------")
    
#     start = datetime.now()
#     print(f"---  HiSTra START at {start}  ---")
    
#     hic_test = test_path
#     if output_path == "":
#         output_path = os.getcwd()
#     else:
#         output_path = os.path.abspath(output_path)
#     matrix_path = output_path
#     testDir_Mat_from_hic = hic2mat(hic_test,matrix_path,juice_path)
    
#     hic_control = control_path
#     if hic_control == "":
#         hic_control = os.path.join(os.getcwd(),'hic_default/GSE63525_IMR90_combined_30.hic')
    
#     print(test_path)
#     print(control_path)
#     print(output_path)
#     print(juice_path)
#     print(deDoc_path)
    
#     controlDir_Mat_from_hic = hic2mat(hic_control,matrix_path,juice_path)
    
#     end1 = datetime.now()
#     print(f"------ Your work directory is {output_path}. ------\n")
#     print(f"------ Your test sample will be dumpped in {testDir_Mat_from_hic}. ------\n")
#     print(f"------ Your control sample will be dumpped in {controlDir_Mat_from_hic}. ------\n")# for debug
#     print(f"--- Step 1 hic2matrix finish. Consuming {end1-start}. --- \n")
    
    
#     ratio500k,testDir_mat_aligned,controlDir_mat_aligned = downsample(testDir_Mat_from_hic,controlDir_Mat_from_hic,0)
#     ratio100k,testDir_mat_aligned,controlDir_mat_aligned = downsample(testDir_Mat_from_hic,controlDir_Mat_from_hic,1)
#     end2 = datetime.now()
#     print(f"------ The matrices are aligen in {testDir_mat_aligned} and {controlDir_mat_aligned}. ------ ")# for debug
#     print(f"--- Step 2 finish. Matrices are aligned. Consuming {end2-end1} ---")
    
#     SV_resultpath = signalFinder(output_path,testDir_mat_aligned,controlDir_mat_aligned)
#     end3 = datetime.now()
#     print(f"------ Translocation score is saved in {SV_resultpath}")
#     print(f"--- Step 3 finish. Raw translocation score are sorted. Consuming {end3-end2}. ---")
    
    
    
    
#     path = '/media/qian/data_sdb4/projects/HiC_SV/HiC_translocation_test/Test/HiST_0.2_demo/Matrix_aligned'
#     deDoc_path = '/home/qian/software/deDoc/deDoc.jar'
#     sv_result_path = "/media/qian/data_sdb4/projects/HiC_SV/HiC_translocation_test/Test/HiST_0.2_demo/SV_result"
#     name_K562 = 'Test_GSE63525_K562_combined_30'
#     Rao_K562_sort = pd.read_csv("../Test/HiST_0.2_demo/SV_result/GSE63525_K562_combined_30/GSE63525_K562_combined_30_result_500k_sorted.csv")
    
#     deDoc_result_path, result_pick_len = deDoc_run(os.path.join(path,name_K562,'100k'), Rao_K562_sort, 0.2, deDoc_path)
#     df_peak_K562 = TLplotandBEDproduce(path,name_K562,Rao_K562_sort[0:result_pick_len])
    
#     for file in os.listdir(SV_resultpath):
#         if fnmatch.fnmatch(file,'*sorted.csv'):
#             sv_result_sort = pd.read_csv(os.path.join(SV_resultpath,file))
    
#     deDoc_result_path, result_pick_len = deDoc_run(os.path.join(testDir_mat_aligned,'100k'), sv_result_sort, 0.4, deDoc_path)
#     df_peak = TLplotandBEDproduce(os.path.dirname(testDir_mat_aligned),os.path.basename(testDir_mat_aligned),sv_result_sort[0:result_pick_len])
#     end4 = datetime.now()
#     print(f"--- Step 4 finish. Translocation boxes are figured out. Consuming {end4-end3}. ---")