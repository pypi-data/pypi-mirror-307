# utils.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" All small functions are including in utils.

Available functions:
- chr_num_int_check: Transfer the chromosome ID to integer, especially 'X' and 'Y' is 23 and 24 respectively.
- chr_str_produce: Transfer the chromosome ID to string, for example, the 1st chromosome is 'chr1', the X chromosome is 'chrX'
- matrix_np2pd: 
- chr_pos2eigen_pos: Given chromosome ID, i.e. 1-22,X,Y return the corresponding position in the eigenvalue dataframe.
- eigen_pos2chr_pos: Given the position in the eigenvalue dataframe, return the chromosome pairs (i,j).
- intra: small function to determine the matrix file is intrachromosome or not. We omit intra matrix.
- sparsefiles: create all interchromosome pairs namelist, including the intrachromosome pairs because it is necessary for depth comparison.
"""

import numpy as np
import pandas as pd
import itertools

def check_pathname_valid(path):
    if path[-1]!='/':
        path = path + '/'
    return path

def chr_num_int_check(chr_i):
    if chr_i not in ['X','Y']:
        chr_i = np.int64(chr_i)
    else:
        chr_i = ord(chr_i)-65
    return chr_i

def chr_str_produce(chr_i):
    if chr_i not in ['X','Y']:
        chr_i = str(np.int64(chr_i))
#     print "chr" + chr_i
    return "chr" + chr_i

def matrix_np2pd(M,chr_i,chr_j):
    M_df = pd.DataFrame(M)
    M_df = M_df.rename_axis(str(chr_i))
    M_df = M_df.rename_axis(str(chr_j),axis="columns")
    return M_df

def chr_pos2eigen_pos(i,j):# i j is chr_num, could be 1-22,X,Y; return x is the corresponding position in the eigenvalue list, eigenvector list
    # if not include intrachromosome, use 46 and finally -1,else use 48.
    if i in ['X']:
        ii = ord(i)-65
    else:
        ii = np.int64(i)
    if j in ['X']:
        jj = ord(j)-65
    else:
        jj = np.int64(j)
    if ii>jj:
        tmp = ii
        ii = jj
        jj = tmp
    return np.int64((46-ii)*(ii-1)/2+jj-ii-1)

def eigen_pos2chr_pos(x,eigen_pair_list): # x is the corresponding position in the eigenvalue list, eigenvector list. Return i j is chr_num, could be 1-22,'X','Y';
    pair = eigen_pair_list[x]
    chr_i = pair.split('--')[0]
    chr_j = pair.split('--')[1]
    return chr_i,chr_j
    # if not incluide intrachromosome, use 22,else use 23 and j=i+xx-1
    # x = x + 1
    # xx = x
    # tmp = 22
    # while (xx>tmp):
    #     xx = xx - tmp
    #     tmp = tmp - 1
    # i = 22-tmp+1
    # j = i+xx
    # if i>22:
    #     chr_i = chr(i+65)
    # else:
    #     chr_i = i
    # if j>22:
    #     chr_j = chr(j+65)
    # else:
    #     chr_j = j
    # return chr_i,chr_j       

def sparsefiles(k,sizes):# k = 0/1, 对应两个分辨率 该函数生成了matrix*/ 下的文件名，包含了一层文件路径
    """ Create a list of filenames.
    Input: k for resolution, 0 is 500k, 1 is 100k; sizes for chromosome details, chrname and res_unit.
    Output: a list like ['*00k/chr1_chr2_*00k.txt']
    """
    chrname = sizes2chrname(sizes)
    res_unit = sizes2resUnit(sizes)
    res_low = res_unit*5
    res_high = res_unit
    resolution = [f"{num2res_sim(res_low)}/",f"{num2res_sim(res_high)}/"]
    R=[f"_{num2res_sim(res_low)}.txt",f"_{num2res_sim(res_high)}.txt"]

    sparse_files = []
    for chri,chrj in itertools.combinations_with_replacement(chrname,2):
        sparse_files.append(resolution[k]+f"{chrname_pre(chri)}"+chri+f"_{chrname_pre(chrj)}"+chrj+R[k])            
    return sparse_files

def intra(name):
    name_split = name.split('/')[1].split('_')
    return name_split[0]==name_split[1]

def sizes2chrname(sizes):
    """ Transfer sizes file into chrname. Make all species available.
    Input: pandas of sizes file;
    Output: array like [chr1, chr2, chr3, ... , chrX](hg19).
    """
    chrname = [sizes[0][i] for i in range(len(sizes))]
    return chrname

def sizes2resUnit(sizes):
    """ Transfer sizes file into resolution unit. Make all species available.
    Input: pandas of sizes file;
    Output: res_unit, e.g hg19 chromosome will be 100000(100k),yeast will be 1000(1k).
    """
    return int(pow(10,len(str(int(np.max(sizes[1])/10000)))))

def num2res_sim(num):
    """ Transfer a integer into string, to simplify the name of files.
    Input: a integer, like 1000,100000;
    Output: a string, like 1k,100k.
    """
    if (num/1000000>=1):
        return str(int(num/1000000))+'M'
    else:
        if (num/1000>=1):
            return str(int(num/1000))+'k'

def chrname_pre(chrname_i):
    """ Make sure chrname_prefix is 'chr'.
    Input: string, like chr1,X;
    Output:string, like '','chr'; to make sure the chrname be "chr1","chrX".
    """
    if chrname_i.startswith('chr'):
        return ''
    else:
        return 'chr'