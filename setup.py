from setuptools import setup, find_packages
from pubgy import __version__ as v

setup(
    name='PUBGy',
    version=v,
    description="PUBG API wrapper for Python",
    long_description="Python wrapper for the PUBG API",
    long_description_content_type="text/markdown",
    url="https://github.com/Discord-ian/pubgy",
    author='Discordian',
    packages=find_packages(exclude=("tests*", "docs*")),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    install_requires=['asyncio', 'aiohttp'],
    python_requires='>=3.5'
)
