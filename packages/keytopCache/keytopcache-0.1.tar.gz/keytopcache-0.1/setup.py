# kt-py-redis\setup.py
from setuptools import setup, find_packages

setup(
    name='keytopCache',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'redis',
    ],
    author='zhangjukai',
    author_email='zhangjukai@keytop.com.cn',
    description='A simple Redis client wrapper for Sentinel and Cluster modes',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)