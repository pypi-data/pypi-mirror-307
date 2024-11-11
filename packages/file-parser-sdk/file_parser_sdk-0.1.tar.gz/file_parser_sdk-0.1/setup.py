
from setuptools import setup, find_packages

setup(
    name="file_parser_sdk",
    version="0.1",
    description="File Parser SDK which is designed to parse various file types and transform them according to provided configuration",
    author="Dinesh Lakhara",
    author_email='dinesh.lakhara@cashfree.com',
    packages=find_packages(exclude=("test", "test.*")),
    install_requires=[
        "boto3==1.12.42",
        "botocore==1.15.49",
        "numpy==1.24.2",
        "pandas==2.0.0",
        "mt-940==4.23.0",
        "xlrd==2.0.1",
        "openpyxl==3.1.2",
        "s3fs==0.4.2",
        "s3transfer==0.3.3",
        "python-dateutil==2.8.2",
        "pytz==2020.1",
        "json-logging==1.2.0",
        "pyzipper==0.3.6",
        "tabula-py==2.1.1",
        "urllib3==1.25.8"
    ],
    python_requires=">=3.6",
)