# coding: utf-8
from setuptools import setup, find_packages

setup(
    name="datalake_sync",
    version="0.1.0",
    author_email='sagar@friscoanalytics.com',
    description="ADLS to Unity Catalog pipeline package",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # Use 'text/x-rst' if your README is in reStructuredText
    url='https://github.com/friscoanalytics-com/ADLS-Connector',
    packages=find_packages(),
    install_requires=[
        "pyspark>=3.0.0",  # PySpark version you're using
         # Delta Live Tables library if you're using Databricks runtime
    ],
    python_requires=">=3.11",
)

