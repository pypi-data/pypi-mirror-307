import os
import numpy

from setuptools import find_packages, setup, Extension


def read(rel_path: str) -> str:
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, rel_path), encoding="utf-8") as fp:
        return fp.read()


def get_version(rel_path: str) -> str:
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


# Package meta-data.
NAME = "frozen-quant"
DESCRIPTION = "A Quantitative Backtest Framework"
REQUIRES_PYTHON = ">=3.10.0"

VERSION = get_version("frozen/__init__.py")

# Detect Cython
try:
    import Cython

    ver = Cython.__version__
    _CYTHON_INSTALLED = ver >= "0.28"
except ImportError:
    _CYTHON_INSTALLED = False

if not _CYTHON_INSTALLED:
    print("Required Cython version >= 0.28 is not detected!")
    print('Please run "pip install --upgrade cython" first.')
    exit(-1)

# What packages are required for this module to be executed?
REQUIRED = [
    "numpy>=1.20.0, <1.24",
    "pandas>=1.5.3",
    "scipy>=1.11.4",
    "statsmodels>=0.14.1",
    "matplotlib>=3.7.1",
    "calplot==0.1.7.5",
    "joypy==0.2.6",
    "mpld3==0.5.10",
    "pyyaml>=6.0.1",
    "nltk>=3.8.1",
    "openpyxl>=3.1.2",
    "dill>=0.3.9",
    "tqdm>=4.66.1",
    "joblib>=1.2.0",
    "tqdm-joblib==0.0.3",
    "numba>=0.59.0",
    "pymongo>=4.6.1",
    "duckdb>=0.10.2",
    # clickhouse only works on MACOS or LINUX
    "chdb>=2.0.4",
    "empyrical==0.4.1",
    "scikit-learn>=1.2.2",
    "chinese-calendar>=1.9.0",
    "holidays>=0.41",
    "pandas_market_calendars>=4.3.3",
    "pdpipe>=0.3.2",
    "quantstats>=0.0.62",
    "tushare>=1.3.7",
    "IPython==8.26.0",
    "setuptools>=75.1.0",
    "optuna>=4.0.0",
]

# Numpy include
NUMPY_INCLUDE = numpy.get_include()

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


# Cython Extensions
extensions = [
    Extension(
        "frozen.factor.extensions._qlibExpr._libs.rolling",
        ["frozen/factor/extensions/_qlibExpr/_libs/rolling.pyx"],
        language="c++",
        include_dirs=[NUMPY_INCLUDE],
    ),
    Extension(
        "frozen.factor.extensions._qlibExpr._libs.expanding",
        ["frozen/factor/extensions/_qlibExpr/_libs/expanding.pyx"],
        language="c++",
        include_dirs=[NUMPY_INCLUDE],
    ),
]

# Where the magic happens:
setup(
    name=NAME,
    version=VERSION,
    license="MIT Licence",
    author="lig",
    author_email="legendarylig@gmail.com",
    url="https://github.com/Mxyzptlk-Z/frozen",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=REQUIRES_PYTHON,
    packages=find_packages(exclude=("tests",)),
    entry_points={
        "console_scripts": [
            "drun=frozen.database.dataflow:run",
            "frun=frozen.workflow:run",
        ],
    },
    # ext_modules=extensions,
    install_requires=REQUIRED,
    extras_require={
        "dev": [
            "prefect>=3.0.3",
            "streamlit>=1.30.0",
            "mlflow",
            "setuptools",
        ],
        "rl": [
            "torch",
        ],
    },
    include_package_data=True,
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.org/classifiers/
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English", 
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
