# -*- coding: utf-8 -*-
"""
weppy-BS3
---------

Add bootstrap3 ui elements to Weppy.
"""

from setuptools import setup

setup(
    name='weppy-BS3',
    version='0.4',
    url='https://github.com/gi0baro/weppy-bs3',
    license='BSD',
    author='Giovanni Barillari',
    author_email='gi0baro@d4net.org',
    description='Bootstrap3 UI elements for weppy',
    long_description=__doc__,
    packages=['weppy_bs3'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'weppy>=0.5',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
