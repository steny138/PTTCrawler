#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

long_description = open('./README.md', 'r').read()
description = ''

setup(name='ptt_crawler',
      version='1.0.0',
      description=description,
      long_description=long_description,
      author='YUCHEN LIU',
      author_email='steny138@gmail.com',
      url='https://github.com/steny138/PTTCrawler',
      packages=['ptt_crawler'],
      package_data={'ptt_crawler': ['*.csv']},
      include_package_data=True,
      license='LICENSE',
      keywords=" " + \
               "",
      install_requires=['python-dateutil==1.5', 'ujson', 'urllib3'],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Environment :: Web Environment',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Financial and Insurance Industry',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: Chinese (Traditional)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Topic :: Office/Business :: Financial :: Investment',
          ],
     )
