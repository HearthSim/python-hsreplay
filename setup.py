#!/usr/bin/env python
import os.path
import hsreplay
from setuptools import setup, find_packages


README = open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "README.md")).read()

CLASSIFIERS = [
	"Intended Audience :: Developers",
	"License :: OSI Approved :: MIT License",
	"Programming Language :: Python",
	"Programming Language :: Python :: 3",
	"Programming Language :: Python :: 3.4",
	"Programming Language :: Python :: 3.5",
	"Topic :: Games/Entertainment :: Simulation",
]

PATCH_VERSION = 1

setup(
	name="hsreplay",
	version="%s.%s" % (hsreplay.__version__, PATCH_VERSION),
	packages=find_packages(),
	author=hsreplay.__author__,
	author_email=hsreplay.__email__,
	description="A library for creating and parsing HSReplay files",
	classifiers=CLASSIFIERS,
	download_url="https://github.com/HearthSim/HSReplay/tarball/master",
	long_description=README,
	url="https://github.com/HearthSim/HSReplay",
	license="MIT",
)
