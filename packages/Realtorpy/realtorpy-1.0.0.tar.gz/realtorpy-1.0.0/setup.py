# Copyright (C) 2024 Lovepreet Gill <labi1240@gmail.com>
# License: MIT, labi1240@gmail.com

from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='Realtorpy',
    version='1.0.0',
    description='Python package for fetching and analyzing REALTOR.CA and REALTOR.COM MLS Listings',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Lovepreet Gill',
    author_email='labi1240@gmail.com',
    license='MIT',
    url='https://github.com/labi1240/Realtorpy',
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=[
        'requests>=2.26.0',
        'pandas>=1.3.5',
        'numpy>=1.21.4',
        'openpyxl>=3.1.2',
        'lxml>=5.1.0',
        'pyyaml>=6.0.1'
    ],
    extras_require={
        "dev": ["twine"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    include_package_data=True,
    package_data={
        'Realtorpy': [
            'config/column_mapping_cfg.json',
            'config/column_mapping_cfg_realtor_com.json',
            'config/graphql_queries.yml'
        ]
    }
)