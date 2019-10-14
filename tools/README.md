# OpenManuscript tools

For more information about these tools, contact david@dhrogers.com.

## Introduction

This is a set of tools that support `openmanuscript` workflows.

## oms2rtf

The `oms2rtf` script creates an `.rtf` file from an `openmanuscript` database. 
To create a *Microsoft Word* document, open the `.rtf` file in *Microsoft Word*,
and then *Save As...* a `.docx` file. This conversion will change the inter-word
spacing of the document, but will otherwise not change anything.

By default, the tool assumes it is being run in the manuscript directory. If
this is not the case, an explicit path must set on the command line. See
examples below.

## oms2docx

This script creates a `.docx` file from an `openmanuscript` database. It is
currently under development, and does not support all features. This is built on
top of `python-dox` and an adapted snippet of html tree parsing code shared in the
comments of that project.

### Known issues

- Mac's `Pages` application does not recognize the `.rtf` footnotes syntax
  output by this application.

## Installation

These tools installs in the normal python way. From the `tools/` directory, run:

```
pip install .
```

## Example

The `example` directory contains a sample `openmanuscript` database, and two
output files - `` and `` - that show the results of the `oms2rtf` workflow.

The following commands use the `example/` directory from this repository, and assume 
that you have installed the tool, per instructions above, and are starting from 
within the `tools/` directory. 

The following command uses all default settings, and will create a file named `manuscript.rtf`. 
This is run within the `example` directory.

```
    cd ../example
    oms2rtf
```

This command creates the manuscript, but this time enables the `footnotes`
option, so that footnotes are printed as needed at the bottom of the page.
```
    cd ../example
    oms2rtf --footnotes
```

This command shows how to use several command line options to override defaults.

```
    cd ../example
    oms2rtf --authorfile a.json --manuscriptfile m.json --outputfile m.rtf
```

This command is run from the `tools` directory, and shows an example in which
`oms2rtf` runs using explicit paths. In this case, the `manuscript.rtf` file will
be written in the `tools` directory.

```
    oms2rtf --manuscriptdir ../example --authorfile a.json --manuscriptfile m.json
```

Finally, this command will create the `manuscript.rtf` file at a specific
location, per the `--outputfile` argument. In this case, it will create the file
in the user's home directory.

```
    oms2rtf --manuscriptdir ../example --authorfile a.json --manuscriptfile m.json --outputfile ~/example_manuscript.rtf
```


