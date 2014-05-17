#!/usr/bin/env python
# coding=utf-8

from distutils.core import setup

setup(
        name='RoboGoby',
        version='0.1',
        author='Travis Libsack',
        url='https://github.com/limbeckengineering/BBB.git',
        modules=['RoboGoby'],
        scripts=[],
        description='test'
)

setup(
        name='BBBgps',
        version='0.1',
        author='Travis Libsack',
        url='https://github.com/limbeckengineering/BBB.git',
        modules=['BBBgps'],
        scripts=[],
        description='GPS module'
)

setup(
        name='Battery',
        version='0.1',
        author='Travis Libsack',
        url='https://github.com/limbeckengineering/BBB.git',
        modules=['BBBgps'],
        scripts=[],
        description='Module used to measure battery life'
)
setup(
        name='BBstepper',
        version='0.1',
        author='Travis Libsack',
        url='https://github.com/limbeckengineering/BBB.git',
        modules=['BBstepper'],
        scripts=[],
        description='Module used to control the stepper motors on the floate'
)
