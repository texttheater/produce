from setuptools import setup, find_packages
setup(
    name="produce",
    version="0.1",
    packages=find_packages(),
    scripts=['produce'],

    # metadata to display on PyPI
    author="Kilian Evang",
    author_email="kilian@evang.name",
    description="Replacement for Make geared towards processing data rather than compiling code",
    license="MIT",
    keywords="make builder automation",
    url="https://github.com/texttheater/produce", 
)
