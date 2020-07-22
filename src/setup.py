import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="openms",
    version="3.1",
    author="David H. Rogers",
    author_email="david@dhrogers.com",
    description="A minimal implementation of OpenManuscript capabilities.",
    long_description="This tool utilizes the data definition for the OpenManuscript project and implements a set of creation capabilities for the OpenManuscript format.", 
    long_description_content_type="text/markdown",
    url="https://github.com/openmanuscript/openmanuscript",
    packages=["openms", "openms.html"],
    scripts=["oms", "oms2outline", "omsedit", "omsnext"],
    install_requires=[
        "markdown",
        "python-docx"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: BSD",
        "Operating System :: OS Independent",
    ],
)