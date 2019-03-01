# The OpenManuscript script

This script creates an `.rtf` file from an `openmanuscript` database. 
The `.rtf` file can be opened by any application that reads `.rtf` files, 
but testing is done only on Microsoft Word.

Note that this script must have write permission in the `openmanuscript`
directory, as well as for the output `.rtf` file that results.

By default, the tool assumes it is being run in the manuscript directory. If
this is not the case, an explicit path must set on the command line. See
examples below.

## Example

The following command will create a file named `manuscript.rtf`, using the
author and manuscript files noted. This is run within the `openmanuscript`
directory.

```
    openms --authorfile author.json --manuscriptfile ms.json
```

This command is run from a location outside the `openmanuscript` directory.

```
    openms --manuscriptdir path/to/manuscript/dir --authorfile author.json --manuscriptfile ms.json
```


