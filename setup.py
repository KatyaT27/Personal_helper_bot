from setuptools import setup, find_packages

setup(
    name='Personalhelper',
    version='1.0',
    packages=find_packages(),
    install_requires=["prettytable"],
    entry_points={"console_scripts": ["personal_helper=personal_helper:main"]}
)
