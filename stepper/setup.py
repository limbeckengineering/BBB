#!/usr/bin/env python
# coding=utf-8

from distutils.core import setup

setup(
	name='BBstepper',
	version='0.1',
	author='Travis Libsack',
	modules=['BBstepper'],
	scripts=[],
	description='Moduke to control steppers using the Beagle Bone Black and Adafruits library'
)

setup(
	name='config',
	version='0.1',
	author='Travis Libsack',
	modules=['config'],
	scripts=[],
	description='Global variables for stepper motors'
)
