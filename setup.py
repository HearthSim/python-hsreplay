#!/usr/bin/env python
import hsreplay
from setuptools import setup, find_packages


CLASSIFIERS = [
	"Intended Audience :: Developers",
	"License :: OSI Approved :: MIT License",
	"Programming Language :: Python",
	"Programming Language :: Python :: 3",
	"Programming Language :: Python :: 3.4",
	"Programming Language :: Python :: 3.5",
	"Topic :: Games/Entertainment :: Simulation",
]

setup(
	name="hsreplay",
	version=hsreplay.__version__,
	packages=find_packages(),
	author=hsreplay.__author__,
	author_email=hsreplay.__email__,
	description="A library for creating and parsing HSReplay files",
	classifiers=CLASSIFIERS,
	download_url="https://github.com/HearthSim/HSReplay/tarball/master",
	url="https://github.com/HearthSim/HSReplay",
	license="MIT",
)
