# The OpenManuscript tool

For more information about this tool, contact david@dhrogers.com.

## Introduction

This script creates an `.rtf` file from an `openmanuscript` database. 
The `.rtf` file can be opened by any application that reads `.rtf` files, 
but testing is done only on Microsoft Word.

Note that this script must have write permission in the `openmanuscript`
directory, as well as for the output `.rtf` file that results.

By default, the tool assumes it is being run in the manuscript directory. If
this is not the case, an explicit path must set on the command line. See
examples below.

## Installation

The tool installs in the normal python way. From the `tools/` directory, run:

```
pip install .
```

## Example

The following examples use the example from this repository, and assume that you
are starting from within the `tools/` directory.

The following command uses all default settings, and will create a file named `manuscript.rtf`. This is run within the `example` directory.

```
    cd ../example
    openms
```

This command shows how to use several command line options to override defaults.

```
    cd ../example
    openms --authorfile a.json --manuscriptfile m.json --outputfile m.rtf
```

This command is run from the `tools` directory, and shows an example in which
`openms` runs using explicit paths. In this case, the `manuscript.rtf` file will
be written in the `tools` directory.

```
    openms --manuscriptdir ../example --authorfile a.json --manuscriptfile m.json
```

Finally, this command will create the `manuscript.rtf` file at a specific
location, per the `--outputfile` argument. In this case, it will create the file
in the user's home directory.

```
    openms --manuscriptdir ../example --authorfile a.json --manuscriptfile m.json --outputfile ~/example_manuscript.rtf
```


