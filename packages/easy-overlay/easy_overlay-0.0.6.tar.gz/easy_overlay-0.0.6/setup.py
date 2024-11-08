from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.6'
DESCRIPTION = 'Python Overlay'
LONG_DESCRIPTION = 'Python overlay that uses pywin32 and ctypes to create an easy to use overlay'

# Setting up
setup(
    name="easy_overlay",
    version=VERSION,
    author="Needlesspage819",
    author_email="<example@example.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pywin32'],
    keywords=['python', 'cheat', 'user_friendly', 'easy', 'windows', 'overlay'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)