# doctor_trans/setup.py

from setuptools import setup, Extension
from Cython.Build import cythonize

# Create the extension for Cython file
ext_modules = [
    Extension(
        name="doctor_trans.trans",
        sources=["doctor_trans/trans.pyx"],  # Path to your .pyx file
    ),
]

setup(
    name='doctor_trans',
    version='0.1',
    packages=['doctor_trans'],
    ext_modules=cythonize(ext_modules),
    install_requires=[
        'pandas',
        'requests',
        'html'
    ],
    author='Nirmal Patel',
    author_email='nirmalpatel1705@gmail.com',
    description='This package translate whole dataframe in any language without any limits.',
    url=''
)
