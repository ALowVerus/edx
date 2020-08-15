from distutils.core import setup
from Cython.Build import cythonize

directives = {'linetrace': False, 'language_level': 3}
setup(ext_modules=cythonize('./computational_geometry/s1_convex_hull/s1_cython_code.py'))
