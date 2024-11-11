from setuptools import setup, find_packages

setup(
  name='lilota-django',
  version='0.0.5',
  packages=find_packages(include=['lilota_django']),
  install_requires=[
    "Django>=5.0.6",
    "lilota>=0.0.5",
  ],
)
