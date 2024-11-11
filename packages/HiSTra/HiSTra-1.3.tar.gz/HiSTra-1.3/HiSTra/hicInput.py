#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Library for reading all args from the command line.

Obtaining all path: 1..hic file path；2. juice_tool path；3. output path；4. deDoc path

Available functions:
- path_get: From command line, reading all path inf.
- usage: Print usage.
- hic2mat: Dumping .hic file with juice_tool, and save them into the output path/Matrix_from_hic, return the path/Matrix_from_hic.
- cool2mat: Dumping .cool/.mcool file with cooler, and save them into the output path/Matrix_from_hic, return the path/Matrix_from_hic.
"""

import sys
import getopt
import argparse
import os
import itertools
import subprocess
from HiSTra.utils import sizes2chrname,sizes2resUnit,num2res_sim,chrname_pre

def hic2mat(hicfile,matrix_path,juice_path,sizes):
    """Transfer the hic file to 276 matrix files.
    Input:
        - hicfile, the abspath of hic file.
        - matrix_path, the output path user set. If empty, use current work directory.
        - juice_path, the juicetools absolute path.
    Output:
        Return Matrix_from_hic dirpath. For example, outputpath(user_set)/Matrix_from_hic/sample_name
    """
    # chrname=[str(i) for i in range(1,23)]
    # chrname.append("X")    # feature-yeast, redefine chrname from sizes.
    chrname = sizes2chrname(sizes)
    res_unit = sizes2resUnit(sizes)
    juice="nohup java -jar "+juice_path 
    res_low = 5*res_unit
    res_high = res_unit
    R500 = f"_{num2res_sim(res_low)}.txt"
    R100 = f"_{num2res_sim(res_high)}.txt"
    fl = os.path.basename(hicfile).split(".")[0] # get sample name
    print(f"--------- The hic file path is {hicfile}. ---------")
    outdir500k = os.path.join(matrix_path,'Matrix_from_hic',fl,f"{num2res_sim(res_low)}")
    if not os.path.exists(outdir500k):
        os.makedirs(outdir500k)
        print(f"Create outdir in resuloutin {num2res_sim(res_low)}...")
    outdir100k = os.path.join(matrix_path,'Matrix_from_hic',fl,f"{num2res_sim(res_high)}")
    if not os.path.exists(outdir100k):
        os.makedirs(outdir100k)
        print(f"Create outdir in resuloutin {num2res_sim(res_high)}...")
    process, cnt = 0, 0
    sum_process = len(chrname)*(len(chrname)-1)/2
    for chri,chrj in itertools.combinations_with_replacement(chrname,2):
        if chrj==chri:
            print(f"--------- We are dumpping {fl} sample chromosome pairs {chri,chrj}.")
            print(f"--------- Process is completed {process*100/sum_process}%... ---------") # for process
            process+=len(chrname)-cnt-1
            cnt+=1

        chri_pre, chrj_pre = chrname_pre(chri), chrname_pre(chrj)
        part1 = ' '.join([juice,'dump observed NONE',hicfile,chri,chrj,f'BP {res_low}',outdir500k])            
        part2 = f"/{chri_pre}"+chri+f"_{chrj_pre}"+chrj+R500 + f' >>juicer_{num2res_sim(res_low)}_log.txt 2>&1 &' 
        command_500k = part1 + part2
        
        part1 = ' '.join([juice,'dump observed NONE',hicfile,chri,chrj,f'BP {res_high}',outdir100k])
        part2 = f"/{chri_pre}"+chri+f"_{chrj_pre}"+chrj+R100 + f' >>juicer_{num2res_sim(res_high)}_log.txt 2>&1 &' 
        command_100k = part1 + part2

        ret500k = subprocess.Popen(command_500k,stderr=subprocess.PIPE,shell=True)
        ret100k = subprocess.Popen(command_100k,stderr=subprocess.PIPE,shell=True)
        a = ret500k.wait()
        b = ret100k.wait()
        if (a!=0):
            print(ret500k.stderr.read().decode('GBK'))
        if (b!=0):
            print(ret100k.stderr.read().decode('GBK'))
        
        if not os.path.exists(outdir500k+f"/{chri_pre}"+chri+f"_{chrj_pre}"+chrj+R500):
            part1 = ' '.join([juice,'dump observed NONE',hicfile,f'{chri_pre}'+chri,f'{chrj_pre}'+chrj,f'BP {res_low}',outdir500k])
            part2 = f"/{chri_pre}"+chri+f"_{chrj_pre}"+chrj+R500 + f' >>juicer_{num2res_sim(res_low)}_log.txt 2>&1 &' 
            command_500k = part1 + part2

            part1 = ' '.join([juice,'dump observed NONE',hicfile,f'{chri_pre}'+chri,f'{chrj_pre}'+chrj,f'BP {res_high}',outdir100k])
            part2 = f"/{chri_pre}"+chri+f"_{chrj_pre}"+chrj+R100 + f' >>juicer_{num2res_sim(res_high)}_log.txt 2>&1 &' 
            command_100k = part1 + part2

            ret500k = subprocess.Popen(command_500k,stderr=subprocess.PIPE,shell=True)
            ret100k = subprocess.Popen(command_100k,stderr=subprocess.PIPE,shell=True)
            a = ret500k.wait()
            b = ret100k.wait()
            if (a!=0):
                print(ret500k.stderr.read().decode('GBK'))
            if (b!=0):
                print(ret100k.stderr.read().decode('GBK'))

    print(f'You can check juicer_{num2res_sim(res_high)}_log.txt and juicer_{num2res_sim(res_low)}_log.txt in current directory if any error occurs.')
    return os.path.join(matrix_path,'Matrix_from_hic',fl)

def cool2mat(coolfile,matrix_path,sizes):
    """Transfer the cool file to 276 matrix files.
    Input:
        - coolfile, the abspath of cool file.
        - matrix_path, the output path user set. If empty, use current work directory.
    Output:
        Return Matrix_from_hic dirpath. For example, outputpath(user_set)/Matrix_from_hic/sample_name
    """
    # chrname=[str(i) for i in range(1,23)]
    # chrname.append("X") 
    chrname = sizes2chrname(sizes)
    res_unit = sizes2resUnit(sizes)
    cooler = "cooler dump -o"
    res_low = 5*res_unit
    res_high = res_unit
    R500 = f"_{num2res_sim(res_low)}.txt"
    R100 = f"_{num2res_sim(res_high)}.txt"
    fl = os.path.basename(coolfile).split(".")[0] # get sample name
    print(f"--------- The cool hic file path is {coolfile}. ---------")
    
    outdir500k = os.path.join(matrix_path,'Matrix_from_hic',fl,f"{num2res_sim(res_low)}")
    if not os.path.exists(outdir500k):
        os.makedirs(outdir500k)
        print(f"Create outdir in resuloutin {num2res_sim(res_low)}...")
        
    outdir100k = os.path.join(matrix_path,'Matrix_from_hic',fl,f"{num2res_sim(res_high)}")
    if not os.path.exists(outdir100k):
        os.makedirs(outdir100k)
        print(f"Create outdir in resuloutin {num2res_sim(res_high)}...")
        
    process, cnt = 0, 0
    sum_process = len(chrname)*(len(chrname)-1)/2
    sleep_procs = []
    for chri,chrj in itertools.combinations_with_replacement(chrname,2):
        if chrj==chri:
            print(f"--------- We are dumpping {fl} sample chromosome pairs {chri,chrj}.")
            print(f"--------- Process is completed {process*100/sum_process}%... ---------") # for process
            process+=len(chrname)-cnt-1
            cnt+=1

        chri_pre, chrj_pre = chrname_pre(chri), chrname_pre(chrj)
        cool500k = outdir500k+f'/{chri_pre}{chri}_{chrj_pre}{chrj}_{num2res_sim(res_low)}_ori.txt'
        cool100k = outdir100k+f'/{chri_pre}{chri}_{chrj_pre}{chrj}_{num2res_sim(res_high)}_ori.txt'
        
        part1 = ' '.join([cooler,cool500k,"-r",f"{chri_pre}{chri}","-r2",f"{chri_pre}{chrj}","-m","--join",f"{coolfile}::resolutions/{res_low}"])
        part2 = f"&& cut -f 2,5,7 {cool500k}>{outdir500k}/{chri_pre}{chri}_{chri_pre}{chrj}{R500} && rm {cool500k}"
        command_500k = part1 + part2
        
        part1 = ' '.join([cooler,cool100k,"-r",f"{chri_pre}{chri}","-r2",f"{chri_pre}{chrj}","-m","--join",f"{coolfile}::resolutions/{res_high}"])
        part2 = f"&& cut -f 2,5,7 {cool100k}>{outdir100k}/{chri_pre}{chri}_{chri_pre}{chrj}{R100} && rm {cool100k}" 
        command_100k = part1 + part2
        # print(command_100k)
        ret500k = subprocess.Popen(command_500k,stderr=subprocess.PIPE,shell=True,close_fds=True)
        sleep_procs.append(ret500k)
        ret100k = subprocess.Popen(command_100k,stderr=subprocess.PIPE,shell=True,close_fds=True)
        sleep_procs.append(ret100k)
        
        # if not os.path.exists(outdir500k+"/chr"+chri+"_chr"+chrj+R500): # debug！I think it's repeated part when I review it after 2 years later.(2024-10-20)
        #     part1 = ' '.join([cooler,cool500k,"-r",f"chr{chri}","-r2",f"chr{chrj}","-m","--join",f"{coolfile}::resolutions/500000"])
        #     part2 = f"&& cut -f 2,5,7 {cool500k}>{outdir500k}/chr{chri}_chr{chrj}_500k.txt && rm {cool500k}"
        #     command_500k = part1 + part2

        #     part1 = ' '.join([cooler,cool100k,"-r",f"chr{chri}","-r2",f"chr{chrj}","-m","--join",f"{coolfile}::resolutions/100000"])
        #     part2 = f"&& cut -f 2,5,7 {cool100k}>{outdir100k}/chr{chri}_chr{chrj}_100k.txt && rm {cool100k}" 
        #     command_100k = part1 + part2
        #     # print(command_100k)
        #     ret500k = subprocess.Popen(command_500k,stderr=subprocess.PIPE,shell=True,close_fds=True)
        #     sleep_procs.append(ret500k)
        #     ret100k = subprocess.Popen(command_100k,stderr=subprocess.PIPE,shell=True,close_fds=True)
        #     sleep_procs.append(ret100k)
            
    for proc in sleep_procs:
        proc.communicate()
        if proc.stdin:
            proc.stdin.close()
        if proc.stdout:
            proc.stdout.close()
        if proc.stderr:
            proc.stderr.close()
        try:
            proc.kill()
        except OSError:
            pass
    return os.path.join(matrix_path,'Matrix_from_hic',fl)

#     part1 = ' '.join(juice,'dump observed NONE',hicfile,chri,chrj,'BP 500000',outdir500k)
#     part2 = "/chr"+chri+"_chr"+chrj+R500 + ' >>juicer_500k_log.txt 2>&1 &' 
    
if __name__ == "__main__":
    input_test_path = "/media/qian/data_sdd/data_sdb4/project/Test_in/mcool/Rao_K562_hg19.mcool"
    input_control_path = "/media/qian/data_sdd/data_sdb4/project/Test_in/mcool/Rao_IMR90_hg19.mcool"
    output_path = "/media/qian/data_sdd/work_dir/TL_output"
    print(cool2mat(input_test_path,output_path))
    print(cool2mat(input_control_path,output_path))
    
    