#!/usr/bin/env python
# coding=utf-8

from distutils.core import setup

setup(
	name='BBstepper',
	version='0.1',
	author='Travis Libsack',
	url='https://github.com/limbeckengineering/BBB/stepper.git',
	modules=['BBstepper'],
	scripts=[],
	description='Module to control stepper motors using the Beagle Bone Black and Adafruits BBIO GPIO library'
)

setup(
	name='config',
	version='0.1',
	author='Travis Libsack',
	url='https://github.com/limbeckengineering/BBB/stepper.git',
	modules=['config'],
	scripts=[],
	description='Global variables for the Project RoboGoby float on the BeagleBone Black.'
)
