#!/usr/bin/env python

import os

from setuptools import setup, find_packages

requirements = []
# with open('requirements.txt', 'r') as f:
#     for line in f.readlines():
#         line = line.strip()
#         requirements.append(line)

setup_requirements = []

test_requirements = []

with open('VERSION') as f:
    VERSION = f.read()

setup(
    author="Ralph Brecheisen",
    author_email='r.brecheisen@maastrichtuniversity.nl',
    python_requires='>=3.11',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    packages=find_packages(include=[
        'emailchecker', 
    ]),
    include_package_data=True,
    # package_data={
    #     'mosamaticdesktop': ['scripts/*', 'VERSION', 'GIT_COMMIT_ID'],
    # },
    description="Logging tool exposed through email",
    install_requires=requirements,
    license="MIT license",
    keywords='emailchecker',
    name='emailchecker',
    setup_requires=setup_requirements,
    tests_require=test_requirements,
    test_suite='tests',
    entry_points={
        'console_scripts': [
            'email-checker=emailchecker.main:main',
        ],
    },
    version=VERSION,
    zip_safe=False,
)