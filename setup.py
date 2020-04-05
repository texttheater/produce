from setuptools import setup, find_packages
setup(
    name="produce",
    version="0.2",
    packages=find_packages(),
    scripts=['produce'],

    # metadata to display on PyPI
    author="Kilian Evang",
    author_email="kilian.evang@gmail.com",
    description="Replacement for Make geared towards processing data rather than compiling code",
    license="MIT",
    keywords="make builder automation",
    url="https://github.com/texttheater/produce", 
)
