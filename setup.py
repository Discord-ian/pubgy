from setuptools import setup
from pubgy import __version__ as v
with open("README.md") as info:
    desc = info.read()
setup(
   name='PUBGy',
   version=v,
   description="PUBG API wrapper for Python",
   long_description=desc,
   long_description_content_type="text/markdown",
   url="https://github.com/Discord-ian/pubgy",
   author='Discordian',
   packages=['pubgy'],
   install_requires=['asyncio', 'aiohttp'],
   python_requires='~=3.5'
)
