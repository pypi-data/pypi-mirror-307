from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='fracodim',
    version='1.1',
    packages=find_packages(),
    author='Renan Gomes',
    author_email='renangcfreitas@gmail.com',
    description='Structural package of the box-counting plot method used in fractal correlation dimension estimation.',
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    url='https://github.com/renangcf/fracodim',
    long_description=long_description,
    long_description_content_type='text/markdown',
)