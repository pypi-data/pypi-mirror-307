import setuptools

_PACKAGE_VERSION = '0.0.1'
_PACKAGE_NAME = 'PythonFileLib'
#_KEYWORDS = "filelib"
_SET_DESCRIPTION = "The file processing collection for Python"

def get_long_description():
    with open("README.md", "r") as fh:
        long_description = fh.read()
    return long_description

def get_using_way():
    with open("PFK-INFO", "r") as fh:
        ways = fh.read()
    return ways

setuptools.setup(
    name = _PACKAGE_NAME,
    version = _PACKAGE_VERSION,
    author = "Sky Yang",
    author_email = "skyprotecter0911@foxmail.com",
    #keywords = _KEYWORDS,
    description = _SET_DESCRIPTION,
    #license = "MIT License",
    platforms = ["Linux", "Windows", "MacOS"],
    long_description = get_long_description(),
    long_description_content_type = "text/markdown",
    #url="https://github.com/israeljcunha/file3",
    packages = setuptools.find_packages(),
    install_requires = [
        "numpy>=2.0.0",
        "pandas>=1.22.0",
        "setuptools>=61.0"
    ],
    classifiers = [
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires = ">=3.7",
    
)
