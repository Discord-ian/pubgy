from setuptools import setup
from pubgy import __version__ as v
with open("README.md") as info:
    desc = info.read()
print(desc)
setup(
   name='PUBGy',
   version=v,
   description="PUBG API wrapper for Python",
   long_description=desc,
   long_description_content_type="text/markdown",
   url="https://github.com/Discord-ian/pubgy",
   author='Discordian',
   author_email='me.discordian@gmail.com',
   packages=['pubgy', 'pubgy.utils'],
   install_requires=['asyncio', 'aiohttp'],
   python_requires='~=3.5'
)
