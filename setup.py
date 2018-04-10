from setuptools import setup, find_packages

setup(
    name='mymodules',
    version='0.1',
    description='Collection of useful modules',
    author='Me',
    license='MIT',
    packages=find_packages(),
    install_requires=['numpy']
)

