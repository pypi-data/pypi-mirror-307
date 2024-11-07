# setup.py
from setuptools import setup, find_packages

setup(
    name='SaskeYT',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
    ],
    entry_points={
        'console_scripts': [
            'SaskeYT=SaskeYT:main',
        ],
    },
    author='Sere22',
    author_email='notengocorreo@gmail.com',
    description='No tengo nada que decir',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/sasukeyt77/PyPI-vamos-a-ver',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',)
