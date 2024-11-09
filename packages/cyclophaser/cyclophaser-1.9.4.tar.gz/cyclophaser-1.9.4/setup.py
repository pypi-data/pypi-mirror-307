from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

VERSION = '1.9.4'
DESCRIPTION = 'Determine phases from extratropical cyclone life cycle'
# LONG_DESCRIPTION = 'This script processes vorticity data, identifies different phases of the cyclone \
    # and plots the identified periods on periods.png and periods_didatic.png'

setup(
    name="cyclophaser",
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Danilo Couto de Souza",
    author_email="danilo.oceano@gmail.com",
    license='MIT',
    packages=find_packages(),
    install_requires=[
        "cmocean>=4.0",
        "contourpy>=1.3",
        "cycler>=0.12",
        "fonttools>=4.53",
        "iniconfig>=2.0",
        "kiwisolver>=1.4",
        "matplotlib>=3.9",
        "numpy>=2.1",
        "packaging>=24.1",
        "pandas>=2.2",
        "pillow>=10.4",
        "pluggy>=1.5",
        "pyparsing>=3.1",
        "pytest>=8.3",
        "python-dateutil>=2.9",
        "pytz>=2024.2",
        "scipy>=1.14",
        "setuptools>=72",
        "six>=1.16",
        "tzdata>=2024.1",
        "wheel>=0.44",
        "xarray>=2024.9"
    ],
    package_data={
        'cyclophaser': ['example_data/example_file.csv'],
    },
    keywords=['cyclone', 'vorticity', 'meteorology', 'atmospherical sciences'],
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
    ],
    project_urls={
        'Documentation': 'https://yourproject.readthedocs.io/en/latest/',
        'Source Code': 'https://github.com/daniloceano/CycloPhaser',
        'Issue Tracker': 'https://readthedocs.org/projects/cyclophaser/',
    },
)
