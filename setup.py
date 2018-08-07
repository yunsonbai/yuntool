# coding=utf-8
import os
from setuptools import setup


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]

setup(
    name="yuntool",
    version="0.4.1",
    packages=get_packages('yuntool'),
    author="yunsonbai",
    author_email='1942893504@qq.com',
    url="http://www.yunsonbai.top",
    description='Tool integration:db data statistics/diagram/email',
    install_requires=[],
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ]
)
