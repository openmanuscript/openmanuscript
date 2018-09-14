import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="openms",
    version="0.9",
    author="David H. Rogers",
    author_email="david@dhrogers.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/openmanuscript/openmanuscript",
    packages=setuptools.find_packages(),
    scripts=["bin/openms"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: BSD",
        "Operating System :: OS Independent",
    ],
)
