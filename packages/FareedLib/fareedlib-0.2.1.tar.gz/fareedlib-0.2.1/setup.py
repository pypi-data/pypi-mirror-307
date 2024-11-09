from setuptools import setup, find_packages
import pathlib

# Read the README file
here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name='FareedLib',  # your library name
    version='0.2.1',
    description='A library with common utilities for string manipulation, list filtering, and basic math operations',
    long_description=long_description,
    long_description_content_type='text/markdown',  # This is important for markdown formatting on PyPI
    author='Fareed',
    author_email='no-email@MrFalafel.com',
    url='https://github.com/MrFalafel/FareedLib',
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
