#!/usr/bin/env python
from setuptools import find_packages
from setuptools import setup

VERSION = "1.0.11"


def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name="pysher_khonik",
    version=VERSION,
    description="Pusher websocket client for python, based on Erik Kulyk's PythonPusherClient with Python2 support",
    long_description=readme(),
    long_description_content_type='text/markdown',
    keywords="pusher websocket client",
    author="Nikita Khorev",
    author_email="khonikdev@gmail.com",
    license="MIT",
    url="https://github.com/khorevnikita/Pysher",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        "websocket-client!=0.49",
        "requests>=2.26.0",
    ],
    tests_requires=["autobahn"],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries ',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
