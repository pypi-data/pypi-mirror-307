from setuptools import setup, find_packages

VERSION = '2.61'

# Setting up
setup(
    name="easy_utils_dev",
    version=VERSION,
    packages=find_packages(),
    install_requires=[
            'psutil' ,
            'ping3' , 
            'flask' , 
            'flask_cors' , 
            'xmltodict' , 
            'paramiko' ,
            'oracledb' ,
        ],
    keywords=['python3'],
    classifiers=[
        "Programming Language :: Python :: 3",
    ]
)