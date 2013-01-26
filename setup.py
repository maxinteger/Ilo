__author__="Vadasz Laszlo"
__date__ ="2010.04.10. 11:20:14"

from setuptools import setup,find_packages

setup (
  name = 'Ilo',
  version = '0.2',
  packages = find_packages(),

  # Declare your packages' dependencies here, for eg:
  install_requires=['foo>=3'],

  # Fill in these to make your Egg ready for upload to
  # PyPI
  author = 'Vadász László',
  author_email = '',

  summary = 'Just another Python package for the cheese shop',
  url = '',
  license = '',
  long_description= 'Long description of the package',

  # could also include long_description, download_url, classifiers, etc.

  
)