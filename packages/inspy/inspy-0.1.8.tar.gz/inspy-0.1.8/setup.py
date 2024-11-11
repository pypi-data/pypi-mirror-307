# -*- encoding: utf-8 -*-
"""
    @File: setup.py \n
    @Contact: yafei.wang@pisemi.com \n
    @License: (C)Copyright {} \n
    @Modify Time: 2024/3/29 11:16 \n
    @Author: Pisemi Yafei Wang \n
    @Version: 1.0 \n
    @Description: None \n
    @Create Time: 2024/3/29 11:16 \n
"""
from setuptools import setup, find_packages

setup(
    name='inspy',  # 包名
    version='0.1.8',  # 包的版本
    author='Yafei Wang',  # 作者名字
    author_email='yafei.wang@pisemi.com',  # 作者邮箱
    description='scan and control for instrument that support SCPI COMMAND added 34461A',  # 简短描述
    long_description=open('README.md').read(),  # 长描述，通常是README
    long_description_content_type='text/markdown',  # 长描述的类型，这里是markdown
    url='https://github.com/AceWalTer/inspy',  # 项目主页
    packages=find_packages(),  # 自动找到项目中的所有包
    include_package_data=True,
    install_requires=[
        # 这里列出了项目的依赖
        'pyvisa>=1.12.0',
        'colorama~=0.4.6',
        'setuptools~=68.0.0'
    ],
    classifiers=[
        # 分类器，用于分类和搜索
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    python_requires='>=3.6',  # Python的最低版本要求
)
