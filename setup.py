#!/usr/bin/env python3
from distutils.core import setup
from setuptools import find_packages

with open("README", "r") as fh:
    long_description = fh.read()

setup(name='exgrex',
      version='0.1.6',
      description='The exgrex package provides the ability to create a test run ' \
                  'of various configurations. Used for external graders as an ' \
                  'entry point to the docker container.',

      long_description=long_description,
      long_description_content_type="text/markdown",
      author='vshagur',
      author_email='vshagur@gmail.com',
      packages=find_packages(exclude=['tests', '*.test.*', '*.test','example_grader',]),
      scripts=['bin/executeGrader', ],
      keywords=['mooc', 'grader', 'python', 'python3'],
      url='https://github.com/vshagur/exgrex',
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: POSIX :: Linux", ],
      )
