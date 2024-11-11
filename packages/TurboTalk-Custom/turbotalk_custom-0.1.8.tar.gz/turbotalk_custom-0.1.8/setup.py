# setup.py

from setuptools import setup, find_packages

setup(
    name='TurboTalk_Custom',
    version='0.1.8',
    packages=find_packages(),
    install_requires=[
        'opyngpt'  # Include any dependencies here
    ],
)
