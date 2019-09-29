#!/usr/bin/env python
from distutils.core import setup
from setuptools import find_packages

setup(name='exgrex',
      version='0.1.0',
      description='The exgrex package provides the ability to create a test run ' \
                  'of various configurations. Used for external graders as an ' \
                  'entry point to the dock container.',

      author='Valeriy Shagur',
      author_email='vshagur@gmail.com',
      # url='https://github.com/vshagur',
      # downloadurl='https://github.com/vshagur',
      # keywords = [‘mooc’, ‘grader’]
      packages=find_packages(exclude=['tests', '*.test.*', '*.test']),
      scripts=['bin/executeGrader', ],
      )
