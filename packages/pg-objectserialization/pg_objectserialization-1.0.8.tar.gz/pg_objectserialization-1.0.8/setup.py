from setuptools import setup, Extension

DIST_NAME = "pg_objectserialization"
DIST_VERSION = "1.0.8"
__author__ = "baozilaji@gmail.com"

setup(
	name=DIST_NAME,
	version=DIST_VERSION,
	description="python game: object serialization",
	author=__author__,
	python_requires='>=3.5',
	install_requires=[
	],
	ext_modules=[
		Extension("pg_objectserialization", sources=["objectserialize.c", "baos.c", "bais.c"], include_dirs=["."])
	]
)
