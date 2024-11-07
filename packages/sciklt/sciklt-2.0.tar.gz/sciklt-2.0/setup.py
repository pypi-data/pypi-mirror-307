from setuptools import setup, find_namespace_packages

setup(name = 'sciklt',
      version = '2.0',
      description = 'Dependency for ML based modules',
      long_description = open("sciklt/README.md", "r").read(),
      long_description_content_type="text/markdown",
      author = 'Anonymus',
      package_data = {'':['licence.txt', 'README.md', 'data\\**']},
      include_package_data = True,
#      install_requires = ['networkx', 'matplotlib', 'scikit-learn == 1.5.2'],
      packages = find_namespace_packages(),
      zip_safe = False)