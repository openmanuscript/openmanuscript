# The OpenManuscript tool

For more information about this tool, contact david@dhrogers.com.

## Introduction

This script creates an `.rtf` file from an `openmanuscript` database. 
The `.rtf` file can be opened by any application that reads `.rtf` files, 
but testing is done only on Microsoft Word.

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
are starting from within the `tools/` directory, and that you have already
installed the tool, per the command above.

The following command uses all default settings, and will create a file named `manuscript.rtf`. This is run within the `example` directory.

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


