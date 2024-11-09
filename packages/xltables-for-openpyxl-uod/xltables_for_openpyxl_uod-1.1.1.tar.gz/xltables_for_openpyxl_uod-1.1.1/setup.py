from setuptools import setup, find_packages


long_description: str

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="xltables-for-openpyxl-uod",
    version="1.1.1",
    author="Chris Massie (Dundee University)",
    author_email="cmassie001@dundee.ac.uk",
    description="More easily work with tables in OpenPyXL.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/UoD-Strategic-Planning-and-Insight/XLTables-for-OpenPyXL",
    packages=find_packages(),
    py_modules=["xltables"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
)
