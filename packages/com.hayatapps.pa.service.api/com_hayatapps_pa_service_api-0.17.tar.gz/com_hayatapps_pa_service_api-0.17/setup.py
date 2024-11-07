from setuptools import setup, find_packages

setup(
    name="com.hayatapps.pa.service.api",
    version="0.17",
    author="Roman Połchowski",
    author_email="rp@hayatapps.com",
    description="PA proto package",
    packages=find_packages(),
    install_requires=[
        'protobuf==5.28.3',
        'grpcio==1.67.1',
        'grpcio-tools==1.67.1'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)