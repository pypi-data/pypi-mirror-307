from Cython.Build import cythonize
from setuptools import setup

files = ["promptools.py"]

setup(name="PromptEngine", ext_modules=cythonize(*files, annotate=True))
