# OpenManuscript tools

For more information about these tools, contact david@dhrogers.com.

## Introduction

This is a set of tools that support `openmanuscript` workflows.

### oms

This script is the standard OMS conversion script, with others being deprecated. Features will be added to this script to support all aspects of the OpenManuscript format.

The script looks at the type of the output file requested, and attempts to write out that type of file. The script will report on failure (if it can't write out that type of file).

By default, the tool assumes it is being run in the manuscript directory. If
this is not the case, an explicit path must set on the command line. See
examples below.

## Requirements

Requirements for this toolset:

- **python 3.x**
- Modules as listed in the ``setup.py`` file. These will be installed
  automatically if ``pip`` setup is used, per instructions.


## Installation 

These tools installs in the normal python way. From the `tools/` directory, run:

```
pip3 install .
```

## Examples

The `example` directory contains a sample `openmanuscript` database, and two
output files - `` and `` - that show the results of the `oms` workflow.

The following commands use the `example/` directory from this repository, and assume 
that you have installed the tool, per instructions above, and are starting from 
within the `tools/` directory. 

The following command uses all default settings, and will create a file named `manuscript.docx`. 
This is run within the `example` directory.

```
cd ../example
oms
```

This command shows how to use several command line options to override defaults.

```
cd ../example
oms --authorfile a.json --manuscriptfile m.json --outputfile m.docx
```

This command is run from the `tools` directory, and shows an example in which
`oms` runs using explicit paths. In this case, the `manuscript.docx` file will
be written in the `tools` directory.

```
oms --manuscriptdir ../example --authorfile a.json --manuscriptfile m.json
```

Finally, this command will create the `manuscript.docx` file at a specific
location, per the `--outputfile` argument. In this case, it will create the file
in the user's home directory.

```
oms --manuscriptdir ../example --authorfile a.json --manuscriptfile m.json --outputfile ~/example_manuscript.docx
```
