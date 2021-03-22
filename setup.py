# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


setup(
    name='xeuledoc',
    version="2",
    packages=find_packages(),
    author="Malfrats",
    install_requires=["httpx"],
    description="Fetch information about a public Google document.",
    include_package_data=True,
    url='https://github.com/Malfrats/xeuledoc',
    entry_points = {'console_scripts': ['xeuledoc = xeuledoc.core:main']},
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
