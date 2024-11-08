


from setuptools import setup, Extension
from Cython.Build import cythonize

setup(
    name='PyGol-ilpp',
    version='1.0',
    ext_modules=cythonize([
        Extension(
            "PyGol-ilpp",               # Name of the extension
            sources=["PyGol-ilpp/PyGol-ilpp.c"],   # Source file(s)
            language="c"         # Specify C++ as the language
        )
    ]),
    zip_safe=False,  # Needed for Cython extensions
)


