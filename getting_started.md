# Getting started

First, install the OpenManuscript modules and commands:

```
    pip3 install openms
```

Next, create an example manuscript:

```
    oms --newmanuscript my_manuscript
```

This will create a directory called `my_manuscript` in the current directory
(assuming you have permission to do so). `cd` into the directory, and create
your first manuscript:

```
    cd my_manuscript
    oms 
```

The `oms` command will take all defaults and create a file called
`manuscript.docx`. Open this with an appropriate tool, and you can see the
result.

You can try the `--settings` option with this example, to demonstrate how a set
of settings can be saved to make things simpler. You can have several settings
files lying around to make it easy to create different types of output.

```
    oms --settingsfile settings.json
```

# Editing your manuscript

Editing your manuscript is now a matter of editing the text files in the
`my_manuscript` directory:

- Edit the scene files to change the content of the scenes.
- Edit the `manuscript.json` or `manuscript.yaml` file to control the content of
  the manuscript, including metadata, scenes, titles, etc.
- Edit the `author.json` or `author.yaml` file to change the author's
  information.

# Creating a Microsoft docx file

Any time you are ready, you can create a `docx` file with the `oms` command. At
first, you can use all the defaults, but as you get more advanced, you can use
the command line to overwrite the options. In addition, you can use
a `settings.json` file to save and execute a set of options. See the
documentation [here](https://github.com/openmanuscript/openmanuscript/blob/master/src/README.md) for more detail.
