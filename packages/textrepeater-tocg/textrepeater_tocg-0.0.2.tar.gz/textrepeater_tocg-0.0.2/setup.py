from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.2'
DESCRIPTION = 'this is a package which lets jou repeat text using the var = repeat(text, amount) command where var is the repeated text, also printrepeat(text, amount) prints the text immediately'

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