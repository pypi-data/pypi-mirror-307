# coding:utf-8

from setuptools import setup, find_packages

with open('Readme.md') as f:
    long_description = f.read()


setup(
        name='testforallen',     # 包名字
        version='1.0',   # 包版本
        description='This is a test of the setup',   # 简单描述
        author='allensrj',  # 作者
        author_email='allensrj@qq.com',  # 作者邮箱
        url='https://github/allensrj/',      # 包的主页
        packages=find_packages(),
        long_description=long_description,
        long_description_content_type='text/markdown',
        license='MIT',
        package_dir={'testforallen': 'src'},

)