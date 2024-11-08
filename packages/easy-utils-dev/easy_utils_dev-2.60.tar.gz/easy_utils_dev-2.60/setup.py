from setuptools import setup, find_packages

VERSION = '2.60'

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
        ],
    keywords=['python3'],
    classifiers=[
        "Programming Language :: Python :: 3",
    ]
)