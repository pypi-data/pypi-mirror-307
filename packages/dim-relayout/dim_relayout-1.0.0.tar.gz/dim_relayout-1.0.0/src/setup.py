#!/usr/bin/python3

#from distutils.core import setup
from setuptools import setup, find_packages

with open("README.rst", "r") as f:
  long_description = f.read()

setup(

    name="dim_relayout",
    version="0.0.3",
    #packages= ["dim_relayout"],
    author="Yingke Huang",
    author_email="ykhuang@ihep.ac.cn",
    description="dim relayout",
    install_requires=[],	# 依赖包会同时被安装
    license='GPL',
    packages=find_packages()
)
