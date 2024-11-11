from setuptools import setup, find_packages

setup(
  name='lilota-django',
  version='0.0.6',
  packages=find_packages(include=['lilota_django']),
  include_package_data=True,
  package_data={
    "lilota_django": ["migrations/*.py"],
  },
  install_requires=[
    "Django>=5.0.6",
    "lilota>=0.0.5",
  ],
)
