import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="OpenManuscript",
    version="1.0",
    author="David H. Rogers",
    author_email="david@dhrogers.com",
    description="A minimal implementation of OpenManuscript capabilities.",
    long_description="This tool utilizes the data definition for the OpenManuscript project and implements a set of creation capabilities for the OpenManuscript format. See https://github.com/openmanuscript/openmanuscript",
    long_description_content_type="text/markdown",
    url="https://github.com/openmanuscript/openmanuscript",
    packages=setuptools.find_packages(),
    scripts=["oms2rtf"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: BSD",
        "Operating System :: OS Independent",
    ],
)
