# -*- coding: UTF-8 -*-
# @Time : 2021/11/24 上午11:44 
# @Author : 刘洪波
import setuptools
from setuptools import setup
from version import _version


with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='pygraphdb',
    version=_version,
    packages=setuptools.find_packages(),
    url='https://gitee.com/maxbanana/graphdb',
    license='Apache',
    author='hongbo liu',
    author_email='bananabo@foxmail.com',
    description='A connect graphdb package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['requests'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
