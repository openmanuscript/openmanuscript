
<img src="img/logo.png" width="80" align="left">

# OpenManuscript

This is OpenManuscript, a text-based data format specification for writing
fiction in an organized, hassle-free way that frees you up to be your most
creative!

For more information about these tools, contact **david *at* dhrogers *dot*
com**.

Project tweets at [@OpenMSProject](https://twitter.com/openmsproject)

## Introduction

This is a specification for OpenManuscript, an ASCII text-based workflow for writing fiction, managing drafts, and creating [fiction manuscripts](https://www.shunn.net/format/story.html).

The OpenManuscript format separates data from the applications that edit,
display or print it, which is a very powerful mechanism for invention.

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

## The Overall Workflow for OpenManuscript
<p align="center">
<img src="img/workflow.png" width="65%">
</p>

As shown in the above diagram, the OpenManuscript format is used by any
compliant editing tool (one that can save text-only files) in the day to day 
work, and when it's time to look at
a final manuscript, share it as a specific document type (Word, PDF, etc.) or
publish it as a final product (ebook, etc.), the writer uses another tool to
create that product.

## Getting Started 

This repository includes: 

- The OpenManuscript specification [document](spec/2-0.md), 
- A command-line based [toolset](tools) for creating manuscripts, 
- An [example](example) of an OpenManuscript database 

The best way to get started is to pull this repository, then explore the
instructions in the [tools](tools) directory, where there are examples and
instructions about a simple toolset.

For more information about these tools, contact **david *at* dhrogers *dot*
com**.

OpenManuscript. Keep it simple.






