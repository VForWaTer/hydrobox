from setuptools import setup, find_packages
import sys

if sys.version_info < (3, 3):
    sys.exit('Python < 3.3 is not supported')

with open('requirements.txt') as fs:
    REQUIREMENTS = fs.read().strip().split('\n')

with open('VERSION.txt') as fs:
    VERSION = fs.read().strip()

with open('classifiers.txt') as fs:
    CLASSIFIERS = fs.read().strip().split('\n')


def readme():
    with open('README.rst') as fs:
        return fs.read()

setup(name='hydrobox',
      version=VERSION,
      license='MIT',
      description='Hydrological toolbox build on top of scipy and pandas',
      long_description=readme(),
      classifiers=CLASSIFIERS,
      author='Mirko Maelicke',
      author_email='mirko.maelicke@kit.edu',
      install_requires=REQUIREMENTS,
      test_suite='nose.collector',
      tests_require=['nose'],
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False
)