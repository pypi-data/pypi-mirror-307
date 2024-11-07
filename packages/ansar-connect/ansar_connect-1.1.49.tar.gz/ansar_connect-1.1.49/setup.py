# Standard PyPi packaging.
# Build materials and push to pypi.org.
# Author: Scott Woods <scott.18.ansar@gmail.com>
import sys
import os
import setuptools
import re

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

README = read('README.rst')

#
#
VERSION_PATTERN = re.compile(r'([0-9]+)\.([0-9]+)\.([0-9]+)')

#
#
PACKAGE = read('PACKAGE')[:-1]

#
#
DESCRIPTION = read('DESCRIPTION')[:-1]

#
#
VERSION = read('VERSION')[:-1]

if not VERSION_PATTERN.match(VERSION):
    print('Version "%s" does not meet semantic requirements' % (VERSION,))
    sys.exit(1)

#
#
DOC_LINK = read('DOC_LATEST_LINK')[:-1]

REQUIRES = [
	"cffi>=1.16.0",
	"PyNaCl>=1.5.0",
	"ansar-create>=1.0.49"
]

setuptools.setup(
	name=PACKAGE,
	version=VERSION,
	author="Scott Woods",
	author_email="ansar.library.management@gmail.com",
	description=DESCRIPTION,
	long_description=README,
	#long_description_content_type="text/markdown",
	#project_urls={
	#	"Documentation": DOC_LINK,
	#},
	classifiers=[
		"Development Status :: 5 - Production/Stable",
		"Intended Audience :: Developers",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: 3.8",
		"Programming Language :: Python :: 3.9",
		"Programming Language :: Python :: 3.10",
		"Programming Language :: Python :: 3.11",
		"Programming Language :: Python :: 3.12",
		"License :: OSI Approved :: MIT License",
		"Operating System :: Linux",
		"Operating System :: macOS",
		"Topic :: Software Development :: Libraries",
	],
	# Where multiple packages might be found, esp if using standard
	# layout for "find_packages".
	package_dir={
		"": "src",
	},
	# First folder under "where" defines the name of the
	# namespace. Folders under that (with __init__.py files)
	# define import packages under that namespace.
	packages=setuptools.find_namespace_packages(
		where="src",
	),
	include_package_data=True,
	entry_points = {
		'console_scripts': [
			'ansar=ansar.command.ansar_command:main',
			'ansar-group=ansar.command.ansar_group:main',
			'ansar-directory=ansar.command.ansar_directory:main',
			'shared-directory=ansar.command.shared_directory:main',
		],
	},
)
