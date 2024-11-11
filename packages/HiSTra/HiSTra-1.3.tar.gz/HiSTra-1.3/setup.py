#!/usr/bin/env python
# -*- coding: utf-8 -*-

# version: 1.3
# author: Qian Yang
# Contact: dtzxyangq@foxmail.com

import os,sys,io
from setuptools import setup,find_packages

VERSION = '1.3'
with open("README.md","r") as f:
    DESCRIPTION = f.read()


tests_require= []
install_requires = ['numpy', 
                    'scipy',
                    'pandas==1.3.5',
                    'matplotlib',
                    'seaborn',
                    'cooler==0.8.11'
                   ]
JAVA_pkgs = {
    "HiSTra":["deDoc/deDoc.jar","juice/juicer_tools_2.09.00.jar"]
}
# JAVA_pkgs = {
#     '':["deDoc/*","juice/juicer_tools_2.09.00.jar"]
# }
setup(name='HiSTra',
      version=VERSION,
      author="Q.Yang",
      author_email='dtzxyangq@foxmail.com',
      keywords='HiC genome structure variation translocation',
      description='Spectral translocation detection of HiC matrices.',
      long_description=DESCRIPTION,
      long_description_content_type="text/markdown",
      license='MIT',
      url='https://github.com/dtzxyangq/HiSTra',
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
      packages=find_packages(),
#       include_package_data=True,
#       package_data={"HiSTra":["deDoc/deDoc.jar","juice/juicer_tools_2.09.00.jar"]},
      scripts=['./HiST'],
      install_requires=install_requires,
      tests_require=tests_require,
#       packages_dir={"":"HiSTra"},
#       packages=find_packages(where="HiSTra"),
      python_requires="==3.8",
     )