#!/usr/bin/env python

from setuptools import setup
from setuptools import find_packages
from asn1tool.version import version


setup(
    name='asn1tool',
    version=version,
    description='ASN.1 parsing, encoding and decoding.',
    long_description=open('README.rst', 'r').read(),
    long_description_content_type="text/x-rst",
    author='Erik Moqvist',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    keywords=['ASN.1', 'asn1'],
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'pyparsing', 
        'typing_extensions'  
    ],
    extras_require={
        'shell': ['prompt_toolkit'],
        'cache': ['diskcache']
    },
    test_suite="tests",
    entry_points={
        'console_scripts': ['asn1tool=asn1tool.__init__:_main']
    }
)

