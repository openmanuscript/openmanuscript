# The OpenManuscript script

This script creates an `.rtf` file from an `openmanuscript` database. 
The `.rtf` file can be opened by any application that reads `.rtf` files, 
but testing is done only on Microsoft Word.

Note that this script must have write permission in the `openmanuscript`
directory, as well as for the output `.rtf` file that results.

The command must be run in the `openmanuscript` directory.

## Example

The following command will create a file named `manuscript.rtf`, using the
author and manuscript files noted.

```
    openms --authorfile author.json --manuscriptfile ms.json
```


