from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'test'

# Setting up
setup(
    name="textrepeater_tocg",
    version=VERSION,
    author="ThatOneCodeGuy",
    author_email="<bentrombouts2012@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[''],
    keywords=['test', 'fun', 'useless', 'python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)