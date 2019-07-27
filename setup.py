from setuptools import find_packages
from setuptools import setup
from z80count.z80count import version


def readme():
    try:
        return open('README.md').read()
    except:
        return ""


setup(
    name="z80count",
    version=version,
    description="A tool to annotate Z80 assembler with cycle counts.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development",
    ],
    keywords="",
    author="Juan J. Martinez",
    author_email="jjm@usebox.net",
    url="https://github.com/reidrac/z80count",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
    ],
    extras_require={
        "dev": [
            "pytest",
            "tox",
        ]
    },
    entry_points={
        "console_scripts": [
            "z80count = z80count.z80count:main",
        ]
    },
)
