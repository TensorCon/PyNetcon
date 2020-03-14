import shutil
import os

from distutils.command.sdist import sdist as sdist_orig
from distutils.errors import DistutilsExecError

from setuptools import setup  

import setuptools.command.build_py


class BuildPyCommand(setuptools.command.build_py.build_py):
  """Custom build command."""

  def run(self):    
    netcon_dir = 'netcon/'
    mex_file = 'netcon_nondisj_cpp.mex'
    object_file = 'netcon_nondisj_cpp.o'
    try:
        self.spawn(['mkoctfile', '--mex', '-O3', 'netcon/netcon_nondisj_cpp.cpp'])
        if os.path.exists(netcon_dir + mex_file):
            os.remove(netcon_dir + mex_file)
        if os.path.exists(netcon_dir + object_file):
            os.remove(netcon_dir + object_file)
        shutil.move(mex_file, netcon_dir)
        shutil.move(object_file, netcon_dir)
    except DistutilsExecError:
        self.warn('mkoctfile failed. Have you installed octave?')
    setuptools.command.build_py.build_py.run(self)


setup(
    name='pynetcon',
    version='0.1',
    url='https://github.com/TensorCon/PyNetcon',
    license='MIT',
    author='David Anekstein',
    author_email='aneksteind@gmail.com',
    packages=['pynetcon'],
    cmdclass={
        'build_py': BuildPyCommand
    },
    install_requires=[
        'oct2py==4.0.6'
    ],
    package_data={'pynetcon':['netcon/netcon.m', 'netcon/netcon_nondisj_cpp.cpp']},
)