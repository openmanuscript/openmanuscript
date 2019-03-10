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

### Known issues

- Mac's `Pages` application does not recognize the `.rtf` footnotes syntax
  output by this application.
- Microsoft Word will discard some of the formatting information when saving in
  `.docx` format. For best results, save either as `.rtf` or `.doc` format
  if converting from `.rtf`

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


