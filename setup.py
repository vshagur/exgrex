#!/usr/bin/env python3
from distutils.core import setup
from setuptools import find_packages


def readme():
    with open('README') as f:
        return f.read()


setup(name='exgrex',
      version='0.1.0',
      description='The exgrex package provides the ability to create a test run ' \
                  'of various configurations. Used for external graders as an ' \
                  'entry point to the dock container.',
      long_description=readme(),
      author='vshagur',
      author_email='vshagur@gmail.com',
      packages=find_packages(exclude=['tests', '*.test.*', '*.test']),
      scripts=['bin/executeGrader', ],
      keywords=['mooc', 'grader', 'python', 'python3'],
      # url='https://github.com/vshagur',
      # downloadurl='https://github.com/vshagur',

      )
