from setuptools import setup, Extension

# Compiles the Python extension.

module = Extension("pyceptron",
		sources = ['pyceptron.c'],
		include_dirs=[],
		library_dirs=[],
		libraries=[]
		)

setup (name = "pyceptron",
	   version = "0.1",
	   description = "Multi-Layer Neural Network for Python.",
	   ext_modules = [module])