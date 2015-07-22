import os
from setuptools import setup, find_packages

# get documentation from the README
try:
    here = os.path.dirname(os.path.abspath(__file__))
    description = file(os.path.join(here, 'README.md')).read()
except (OSError, IOError):
    description = ''

dependencies = ['gaiatest-v2.0',
                'fxapom==1.4']

setup(name='marketplacetests',
      version='1.0',
      description="Gaia UI test for Marketplace",
      long_description=description,
      classifiers=[],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='mozilla',
      author='WebQA Team and contributors',
      author_email='gaia-ui-automation@mozilla.org',
      url='https://wiki.mozilla.org/QA/Execution/Web_Testing',
      license='MPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      install_requires=dependencies)
