# setup.py
from setuptools import setup, find_packages

setup(
    name='yuxin_helpers',
    version='0.1.5',
    packages=find_packages(),
    author='Yuxin Geng',
    author_email='yuxin.evol@gmail.com',
    description='Yuxin\'s helper package with utilities for diverse tasks.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yuxingeng/yuxin_helpers',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
