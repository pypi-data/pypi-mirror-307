import os
from setuptools import setup

from binance import __version__

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def read_requirements(filename):
    with open(filename) as f:
        return f.read().splitlines()


settings = dict(
    name='binance-sdk-proxy',
    packages=[
        'binance',
        'binance/apis',
        'binance/client',
        'binance/common',
        'binance/handlers',
        'binance/processors',
        'binance/subscribe',
    ],
    version=__version__,
    author='Master Duck',
    author_email='you-dont-know-who@gmail.com',
    description='Binance Python SDK',
    install_requires=read_requirements('requirements.txt'),
    tests_require=read_requirements('test-requirements.txt'),
    extras_require={
        'pandas': ['pandas']
    },
    license='MIT',
    keywords='binance exchange sdk rest api bitcoin btc bnb ethereum eth neo',
    url='https://github.com/mastergod/binance-sdk',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    python_requires='>=3.7',
    classifiers=[
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
    ]
)


if __name__ == '__main__':
    setup(**settings)
