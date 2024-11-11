# sdk/setup.py

from setuptools import setup, find_packages

setup(
    name='ixlab-tradingSDK',  # Use hyphens for PyPI package names
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'aiohttp>=3.7.4'
    ],
    url='https://github.com/iX-LAB-Official/trading_sdk',
    license='MIT',
    author='iX LAB',
    author_email='info@ixlab.ai',
    description='A Python SDK for interacting with the iX LAB trading API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
