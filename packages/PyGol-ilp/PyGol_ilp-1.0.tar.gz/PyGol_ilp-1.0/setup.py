


from setuptools import setup, Extension
from Cython.Build import cythonize

setup(
    name='PyGol_ilp',
    version='1.0',
    ext_modules=cythonize([
        Extension(
            "PyGol_ilp",               # Name of the extension
            sources=["PyGol_ilp/PyGol_ilp.c"],   # Source file(s)
            language="c"         # Specify C++ as the language
        )
    ]),
    zip_safe=False,  # Needed for Cython extensions
)


