from setuptools import setup, find_packages

setup(
    name='dlcalab',
    version='3.0',
    packages=find_packages(),
    install_requires=[],
    package_data={'dlcalab': ['*.py', '*.ipynb', '*.csv', '*.jpg']},
)
