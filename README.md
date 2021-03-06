[![Build Status](https://travis-ci.com/openmanuscript/openmanuscript.svg?branch=master)](https://travis-ci.com/openmanuscript/openmanuscript)

<img src="img/logo.png" width="80" align="left">

# OpenManuscript

Welcome to the *OpenManuscript* project, a data format and a set of command line
tools that help you write fiction in a way that works with you to be your most
creative and efficient in getting words on the page.

I've been writing long enough to want to solve a few long-term problems:

- Years ago I worked on an awesome story idea, but I was using an old Word
  version, and I can't open the files anymore.

- Let's face it, lots of text editing software wasn't designed with writing 
  fiction manuscripts in mind. It's tough to change things around (like the 
  order of scenes or chapters), tough to compare versions of things, and 
  tough to maintain multiple versions of things.

- If you're a writer, you have a favorite text editor, and you'd like to use
  that one, even if you're ultimately going to create a *docx* file. And, hey - 
  maybe you'd like to use different editors. It shouldn't matter ...

Isn't there a simple way to write manuscripts by just editing text files? Why do
I have to tie myself to a specific word processor, workflow, or other tool?

So that's where this project came from ...

## This Project

This is a specification for OpenManuscript, an ASCII text-based workflow for 
writing fiction, managing drafts, and creating 
[fiction manuscripts](https://www.shunn.net/format/story.html).

The OpenManuscript format separates data from the applications that edit,
display or print it, which is a very powerful mechanism for invention.

To dig in, just [get started with a simple example](getting_started.md). Or,
take a look a [this example workflow](workflow.md) if you're interested in that.

## Advantages of OpenManuscript

The advantages of the OpenManuscript format are many:

- OpenManuscript is an open standard, using only common text-based file formats.
  - Currenly, only **JSON** and **Markdown** files are needed. We use
    [Gruber's](https://daringfireball.net/projects/markdown/) specification of
    markdown.
- The author can use favorite tools for editing text, **markdown** and **JSON**
  files.
- The author can build a manuscript from scenes and chapters, in a way that
  works for that author.
  - The basic unit of writing in OpenManuscript is the **scene**, so an author
    can easily compare different chapter/scene orders, combinations and versions 
    with minimal effort. This is a huge advantage over writing workflows based on, 
    for example, Microsoft Word.


## Getting Started 

As we said before, to dig in, just [get started with a simple example](getting_started.md). Or,
take a look a [this example workflow](workflow.md) if you're interested in that.

This repository includes: 

- The OpenManuscript specification [document](spec/2-0.md), 
- A command-line based [toolset](src) for creating manuscripts, 
- An [example](example) of an OpenManuscript database 
- Instructions for [getting started](getting_started.md). 
- An [example workflow](workflow.md) that shows how you can use these
  tools and data specification in a real write-submit-edit workflow.

The best way to get started is to pull this repository, then explore the
instructions in the [src](src) directory, where there are examples and
instructions about a simple toolset.

For more information about these tools, contact **david *at* dhrogers *dot*
com**.

OpenManuscript. Keep it simple.

## Contact

For more information about these tools, contact **david *at* dhrogers *dot*
com**.

Project tweets at [@OpenMSProject](https://twitter.com/openmsproject)
