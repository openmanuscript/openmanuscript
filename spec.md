This is a specification for Open Manuscript v1.0, a database for a text-based workflow for creating manuscripts. There are a set of required and optional directories and files. This specification allows other files and directories to be present under the main manuscript directory, but they are not part of this  specification. 

At the most basic level, a manuscript is a pairing of an author and a sequence
of chapters. Meta data tags throughout the specification capture additional data
that can be included to enrich a properly formatted manuscript.

**OPEN MANUSCRIPT DATA SPECIFICATION**

The Open Manuscript data specification is a set of files and directories contained within a single top level directory.

- **manuscript directory** (required). Top level directory. This is 
  the top level of the data. This specification imposes no restrictions on 
  naming this directory.

- **author_file** (required). A properly formatted `JSON` file describing the 
  author of this manuscript. The specification is below. Name is not specified
  by this document. There must be at least one author file.

- **manuscript_file** (required). A properly formatted `JSON` file that 
  describes the names and order of the chapters, and which scenes go into 
  them. The specification is below. Name of this file is not specified by this
  document. There must be at least one manuscript file.

- **scans/** (optional). This is a directory for scanned pages that can be 
  incorporated into the manuscript. The assumption is that a single scan is
  a scan of a full page of notes, a typewritten page, or other non-digital
  writing. Scans can be one of the supported image types: [.pdf, .jpg, .png].

- **scenes/** (required). This is a directory containing scene files. There may 
  be unused scenes (scenes not noted in a `manuscript` file).
  
```
    EXAMPLE of manuscript data

    adventure/
        author.json
        manuscript.json
        scans/
            001.pdf
            002.png
            ...
        scenes/
            001.md
            002.md
            003.md
            start.md
            this_scene.md

```

**AUTHOR.JSON File**
The content of the value for each key is not examined for correctness - each is simply treated as a string. Each must follow proper `JSON` formats for strings.

- **version** (required) the version of this specification the file follows. 

- **author** A JSON object. The following [key,value] pairs define an author's
  data.
    - **name** The author's full name. Can be a list of names. The string is not checked for any formatting constraints (required).
    - **surname** A single name, to be included in the header for each manuscript page, per standard manuscript formatting (required).
    - **email** The author's email address (required).
    - **phone** The author's phone number (required).
    - **website** The author's website (optional).
    - **addressCountry** The address' country" (required). 
    - **addressLocality** The address' locality (city) required).
    - **addressRegion** The address' region (state) (optional). As needed, if the country has entities such as states.
    - **postalCode** Zip or other postal code (required).
    - **streetAddress** Street address (required).
    - Other valid `JSON` data may be present, but is not part of this    specification. 

- Other valid `JSON` data may be present, but is not part of this    specification. 


```
    SPECIFICATION of author.json file

    {
    "version" : String, 
    "author" : {
        "name"      : String, 
        "surname"   : String,
        "email"     : String,
        "phone"     : String,
        "website"   : String,
        "addressCountry"    : String,
        "addressLocality"   : String,
        "addressRegion"     : String,
        "postalCode"        : String,
        "streetAddress"     : String
    }
    }


    EXAMPLE of author file

    {
    "version" : "1.0",
    "author" : {
        "name"      : "Ima Q. Writer",
        "surname"   : "Writer",
        "email"     : "imaqwriter@imawriter.com",
        "phone"     : "(000) 000-0000",
        "website"   : "www.imawriter.com",
        "addressCountry"    : "USA",
        "addressLocality"   : "Writerville",
        "addressRegion"     : "NM",
        "postalCode"        : "88888"
        "streetAddress"     : "111 Writer's Way"
    }
    }
```

**MANUSCRIPT file**
The manuscript file defines a series of chapters, each of which is made up of
scenes.

- **version** the version of this specification the file follows. 
- **manuscript** A JSON object. The following [key,value] pairs define
  a manuscript's data.
    - **title** The full title of the manuscript.
    - **runningtitle** A one word title, included in each page's header, per common manuscript formatting. 
    - **chapters** A list of chapters. a `chapter` is defined below. A chapter is an array of scenes, with metadata. 
    - Other valid `JSON` data may be present, but is not part of this    specification.

```
    SPECIFICATION of manuscript.json file
    {
    "version" : String, 
    "manuscript" : {
        "title" : String, 
        "runningtitle" : String, 
        "chapters" : Array.of(Chapter),
        ]
    }
    }

    EXAMPLE
    {
    "version" : "1.0",
    "manuscript" : {
        "title" : "Finding the Story: A Novel",
        "runningtitle" : "finding",
        "chapters" : [
            {
                "title"  : "A Time for Starting",
                "scenes" : ["001", "002", "003", "004", "005"],
                "desc"   : "Our first encounter with the Main Character.",
                "story"  : "Meet MC, learn of inner desire and conflict.",
                "tod"    : "Sunrise",
                "setting": "Deck of the ship Foundation",
                "pov"    : "Melvin",
                "tags"   : ["introduction", "final"]
            }
        ]
    }
    }
```


**CHAPTER** 
A chapter is a collection of scene files, with additional optional metadata.
Chapters are numbered automatically based on their order in the file.
Scenes are included in the order that they appear in the scene list.

- **desc**  A short description of the chapter, to be used in outlines.
- **pov**   Point of view of the chapter. Any string is valid.
- **scenes** An array of scene names. These are expected to be present in the
  `scenes` directory, but this is not strictly required by the specification. 
- **setting** The setting of the scene. Any string is valid.
- **story** A description of the story points in a scene. This is used for 
   notes to the author, and is not included in the outline.
- **tags** An array of strings used to define collections of chapters.
- **title** The title of the chapter.
- **tod** Time of day. Any string is valid.
- Other valid `JSON` data may be present, but is not part of this    
  specification.

```
    CHAPTER specification

    {
        "desc"    : String, 
        "pov"     : String, 
        "scenes"  : Array.of(String),
        "setting" : String, 
        "story"   : String, 
        "tags"    : Array.of(Strong) 
        "title"   : String, 
        "tod"     : String
    }
```
**SCENE.MD file**
A scene file is *required* to be a text-only file using a subset of
markdown for any formatting (bold, italic, lists, footnotes or endnotes,
etc.) The following markdown must be supported by any application that
implements this specification. All other markdown is ignored by
OpenManuscript-compliant applications, and can be handled by extensions or other
applications. 

- bold 

```
        Here is a bold word: **word** 
```
    
- italic 

```
        Here is an italicized word: *word* 
```

- ordered lists

```
        1. first
        2. second
        3. third
```

- unordered lists

```
        - first
        - second
        - third
```

- footnote or endnote 

```
        This is a sentence, with a footnote[^ this is a footnote]
        This is another sentence, with a footnote[^check]

        [^check]:If you have a long note, you can put it in another place
        in the document, like maybe at the bottom of the doc. Any application
        that reads, writes or displays OpenManuscript format handles this.
```

- links

```
        [Here is a link.](http://www.link.com)
        [Here's another way of doing it.][1]
        And one more [way to do it].
        And one that you can parse [yourself].

        [1]: http://something.com
        [way to do it]: http://another_something.com
        [yourself]: This can contain anything, and you can do ... anything 
```
