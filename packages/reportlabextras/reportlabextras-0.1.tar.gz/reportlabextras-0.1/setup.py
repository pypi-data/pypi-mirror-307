from setuptools import setup, find_packages
setup(
name='reportlabextras',
version='0.1',
author='Bohdan Paris',
description='Adds the ability to have inbuilt fractions and powers written within the PDF itself for mathematical purposes.',
packages=find_packages(),
install_requires =[
    'reportlab>=4.2.2'
],
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
python_requires='>=3.6',
)