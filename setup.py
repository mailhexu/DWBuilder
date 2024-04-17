from setuptools import setup, find_packages
from os.path import abspath, dirname

setup(
    name='dwbuilder',
    version='1.1.0',
    author='M.Z.Khalid',
    author_email='zeeshan.khalid039@gmail.com',
    description='A package for developing domain wall structures for atomistic calculations',
    license='MIT',
    packages=find_packages(),
    install_requires=['ase','numpy','matplotlib'],
    entry_points={
        'console_scripts': [
            'dwbuilder = scripts.dwbuilder:main',
            'dbuilder = scripts.dbuilder:main',
            'hibuilder = scripts.hibuilder:main',

        ]
    }
)

