# An Example Workflow

Any writing workflow has a few main parts:

1. [Content creation/editing](#content-creation/editing)
2. [Submission](#submission)
3. Repeat

As a collection of data, a manuscript also requires:

1. [Reliable backup](#reliable-backup)
2. [Long term accessibility](#long-term-accessibility) (can you open the files 5 or 10 years from now)

This example workflow shows how you might achieve this with the *OpenManuscript*
data format and the *OMS toolset*.

The big thing to remember is that you can save files in the top level manuscript 
directory, and those files will be ignored by any tools designed to work on the
*OpenManuscript*. So, you can save notes and information in an organized way
that makes sense to you.

## File data types

Everything you'll create is a text-based file, but there are a few data types
you'll need to know about:

1. [Markdown](https://daringfireball.net/projects/markdown/), which is a way of
adding **bold** and *italics* to your files, among other simple things.
2. [YAML](https://en.wikipedia.org/wiki/YAML) or [JSON](https://en.wikipedia.org/wiki/JSON) 
files for manuscript and author files. **yaml** is probably a better choice if you're 
just starting out, as it is a human-readable file format, but it's your choice.

## Content Creation/Editing

To get started, you can create a manuscript directory like this:

```
    oms --newmanuscript my_novel
```

From then your main editing will consist of creating and editing scenes, and then creating
a manuscript that includes those scenes. Here's how you might work:

1. Create a new file in `scenes` directory, and just write. 
2. When you're ready, edit the manuscript file to include that scene. Either 
add the scene to the list of scenes in an existing chapter, or create a new 
chapter that includes this scene. 
3. Check your work by creating the manuscript with **oms**.

### Creating alternate manuscripts

If you want to compare different organizations of chapters and scenes, you can
create multiple manuscript files in the directory that have the different
organizations. An *OpenManuscript* directory with more than one manuscript file
might look like this:

```
    my_novel/
        high_drama_version.json
        slow_burn_version.json
        scenes/ 
            (all of the scene files)
```

To create the manuscripts, you would run the following commands from within the
`my_novel` directory:

```
    oms --manuscriptfile high_drama_version.json
    oms --manuscriptfile slow_burn_version.json
```

This allows you to create and maintain different versions of the manuscript to
just try out, using the same scenes as building blocks.

## Submission

When it's time to submit a *docx* or *pdf* file to an editor, agent, or
magazine, you can create one with the `oms` tools in this repository. Then it's
up to you to keep track of that manuscript.

To do this, you can simple create
a directory, name the file something meaningful, and keep it around. You can
also edit a small file that contains notes (in this example, it's called
`readme.me`) that remind you what each of the submission files was for. For
example:

```
    my_novel/
        high_drama_version.json
        slow_burn_version.json
        scenes/ 
            (all of the scene files)
        submissions/
            readme.md
            2020-08_submission-to-jane.docx
            2019-08_submission-to-john.docx
            ...
```


## Version Control and Management

If you're interested in more fine-grained version control of manuscript files,
scenes, and the like, you can use *OpenManuscript* in conjunction with a version
control system like [git](https://github.com), if you know that system. The data
format works well by creating a repository for each manuscript. You can then use
tags and versions to track manuscripts and scene versions and options more
easily.

## Reliable Backup

The *OpenManuscript* data specification and tools *do not manage backup*, but
instead, like most modern software, rely on third party software to reliably
backup your work. Modern web-based backups like [Dropbox](https://dropbox.com) 
and [Google Drive](https://google.com/drive) (among many others), are reliable
and low-cost (even free!) methods to back up files.

To back up your *OpenManuscript* files, simply set up your backup service to
manage the directory that contains your files. For example, you can save all
your writing under one directory, and set up your backup service to manage the
highest level directory:

```
    my_writing/ (this is the directory that should be backed up)
        manuscript_one/   
        manuscript_two/   
        manuscript_three/   
``` 

## Long Term Accessibility

The *OpenManuscript* format is designed to be accessible over the long term, as
it relies on the most basic data formats (text files) and data types (MarkDown,
JSON, and YAML). This data should be accessible with the most basic tools that
available on most computers.

The *OMS* toolset is written in Python, which is a very common scripting
languge, and the tools are simple enough that they can be updated by many
programmers. The toolset is open source, so in the event that the tools are
abandonded by the developer, they can be adopted by any interested party and
reliably updated. This is based on the general philosophy of open source software.
