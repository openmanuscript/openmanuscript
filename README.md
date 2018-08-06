
<img src="https://github.com/moonimal/openmanuscript/blob/master/img/logo.png"
width="80" align="left">

# OpenManuscript

This is OpenManuscript, a text-based data format specification for writing
fiction, and turning them into manuscripts.

For more information about this specification, contact david@dhrogers.com.

## Introduction

This is a specification for OpenManuscript v1.0, a database for an ASCII text-based workflow for creating manuscripts. 

Using the OpenManuscript format separates the writing from the application used to edit, display and print it, which is a very powerful mechanism for invention. With this format, a variety of tools can work on the same data, and a writer can switch between tools, creating a workflow that best supports an individual writer's specific way of crafting novels. 

The vision for this data format is to provide a text-based, flexible way of
capturing, organizing and promoting the sometimes chaotic progression of ideas
that go into making a novel. The OpenManuscript format is text-based, so it
isn't locked behind the firewall of a particular application. Rather, it is
a format that can be edited by simple tools, compiled into any format, and
returned to again and again over time. Using a text-based standard means
the author needn't worry that the format will be unreadable down the road
because the software you used outdated, no longer reads that version of the
output, or is simply gone. 

At the most basic level, a manuscript is a pairing of an author and a sequence
of chapters, and this is represented in the basic structure of the
OpenManuscript format. The format assumes you'll write lots of scenes, trying
them out in different sequences of chapters. It's easy to have different
arrangements of different scenes so that you can quickly compare them. Meta data tags throughout the specification capture additional data that can be included to enrich a properly formatted manuscript.

OpenManuscript defines a set of required and optional directories and files,
but can be extended by including other information, which can be ignored by
applications that don't know about it.

This repository includes a specification document, as well as an example of the
file format.






