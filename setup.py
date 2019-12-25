from distutils.core import setup, Extension
from Cython.Build import cythonize
import numpy

setup(
    ext_modules=[
        Extension("module_change_detection", ["module_change_detection.c"],
                  ext_modules=cythonize("module_change_detection.pyx"),
                  include_dirs=[numpy.get_include()]
                  ),
    ]
)
#
# setup(
#     ext_modules=cythonize("lee_filter_c.pyx"),
#     include_dirs=[numpy.get_include()]
# )
