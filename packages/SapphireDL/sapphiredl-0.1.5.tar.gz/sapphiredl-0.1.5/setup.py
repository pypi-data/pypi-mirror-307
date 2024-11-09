from setuptools import setup, find_packages

setup(
    name='SapphireDL',
    version='0.1.5',
    author='Albert',
    description='Library for simple DL structure',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/itbert/Sapphire-DL',
    packages=find_packages(),
    install_requires=[
        'numpy~=2.1.2',
        'setuptools~=75.3.0'
    ]
)
