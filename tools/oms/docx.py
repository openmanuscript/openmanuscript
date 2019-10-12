from . import core

import os
import json
import re

from docx import Document
from docx.shared import Inches, Pt
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.text import WD_LINE_SPACING
from docx.enum.section import WD_SECTION
from docx.oxml.shared import OxmlElement, qn

# -----------------------------------------------------------------------------
# globals
# -----------------------------------------------------------------------------

MARGIN = {
    "page" : 1,
}

# the following three fuctions add page numbers, thanks to:
# https://stackoverflow.com/questions/56658872/add-page-number-using-python-docx
#
def create_element(name):
    return OxmlElement(name)

def create_attribute(element, name, value):
    element.set(qn(name), value)

def add_page_number(run):
    fldChar1 = create_element('w:fldChar')
    create_attribute(fldChar1, 'w:fldCharType', 'begin')

    instrText = create_element('w:instrText')
    create_attribute(instrText, 'xml:space', 'preserve')
    instrText.text = "PAGE"

    fldChar2 = create_element('w:fldChar')
    create_attribute(fldChar2, 'w:fldCharType', 'end')

    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
#
# end of stackoverflow solution. Thanks!
#

def add_page_slug_header(section):
    # section.different_first_page_header = True
    header = section.header
    p = header.add_paragraph()
    p.add_run("{}/ {}/ ".format(core.author["surname"], core.
                manuscript["runningtitle"].upper()))
    run = p.add_run()
    add_page_number(run)

    pf = p.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.RIGHT

def debug_sections(document):
    print("WORD: debugging sections ...")
    cur = 0
    for section in document.sections:
        print("Section {}".format(cur))
        print("{}".format(section.start_type))
        cur = cur + 1

def add_section(document, s_type):
    new_section = document.add_section(s_type)
    # set margins 
    new_section.top_margin    = Inches(MARGIN["page"])
    new_section.bottom_margin = Inches(MARGIN["page"])
    new_section.left_margin   = Inches(MARGIN["page"])
    new_section.right_margin  = Inches(MARGIN["page"])
    header = new_section.header
    header.is_linked_to_previous = False

    add_page_slug_header(new_section)

def write_title(document):
    p = document.add_paragraph("{}\n{}\n{}, {} {}\n{}\n{}\n".format(
                            core.author["name"],
                            core.author["streetAddress"],
                            core.author["addressLocality"], 
                            core.author["addressRegion"], 
                            core.author["postalCode"],
                            core.author["phone"],
                            core.author["email"]))

    pf = p.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf.line_spacing_rule = WD_LINE_SPACING.SINGLE

    for i in range(0, 9):
        document.add_paragraph()

    p = document.add_paragraph()
    pf = p.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf.line_spacing_rule = WD_LINE_SPACING.DOUBLE
    run = p.add_run(core.manuscript["title"])

    p = document.add_paragraph()
    pf = p.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf.line_spacing_rule = WD_LINE_SPACING.DOUBLE
    run = p.add_run("by")

    p = document.add_paragraph()
    pf = p.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf.line_spacing_rule = WD_LINE_SPACING.DOUBLE
    run = p.add_run("{}".format(core.author["name"]))

    # set page margins
    # for now, this should be the only section
    for section in document.sections:
        section.top_margin    = Inches(MARGIN["page"])
        section.bottom_margin = Inches(MARGIN["page"])
        section.left_margin   = Inches(MARGIN["page"])
        section.right_margin  = Inches(MARGIN["page"])

def write_chapter_heading(document, chapter, chapnum, chaptype):
    chapnum = "CHAPTER {0}".format(chapnum).upper()
    document.add_page_break()

    for i in range(0, 10):
        p = document.add_paragraph()
        pf = p.paragraph_format
        pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
        pf.line_spacing_rule = WD_LINE_SPACING.SINGLE

    if (chaptype == "CHAPTER"):
        allcaps_title = chapnum
        chaptername   = chapter["title"]
    else:
        allcaps_title = chaptype
        chaptername   = ""

    p = document.add_paragraph()
    pf = p.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf.line_spacing_rule = WD_LINE_SPACING.DOUBLE
    run = p.add_run(allcaps_title)
    run.bold = True

    p = document.add_paragraph()
    pf = p.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf.line_spacing_rule = WD_LINE_SPACING.DOUBLE
    run = p.add_run(chaptername)
    run.bold = True

    p = document.add_paragraph()


def write_preamble(doc):
        # Set up the document
        style     = doc.styles['Normal']
        font      = style.font
        font.name = core.settings["font"]
        font.size = Pt(int(core.settings["fontsize"]))

        # Styles
        styleIndent = doc.styles.add_style('Indent', WD_STYLE_TYPE.PARAGRAPH)
        pf = styleIndent.paragraph_format
        pf.line_spacing_rule = WD_LINE_SPACING.DOUBLE
        # pf.left_indent = Inches(0.25)
        pf.first_line_indent = Inches(0.5)
        pf.space_before = Pt(12)
        pf.widow_control = True

def write_postamble(doc):
    print("WORD: write_postamble (no-op)")

def write_docinfo(doc):
    print("WORD: write_docinfo (no-op)")

def write_chaptersummary(doc, chapter, chapnum, chaptype):
    print("WORD: write_chaptersummary (no-op)")

# -----------------------------------------------------------------------------
# write a scene separator
# -----------------------------------------------------------------------------
def write_scene_separator(doc, scene):
    separator = "###"

    if core.settings["filescenesep"]:
        separator = scene

    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf.line_spacing_rule = WD_LINE_SPACING.DOUBLE
    run = p.add_run(separator)


# -----------------------------------------------------------------------------
# write a single scene
# -----------------------------------------------------------------------------
def write_scene(doc, scene):
    scenefile = core.get_scenefile(scene)

    if os.path.isfile(scenefile):
        with open(scenefile, "r") as sfile:
            data = sfile.read()
            # handle everything
            # count the number of words in the file
            count = data.split()
            data = data.strip()
            split = data.split("\n\n")
            for paragraph in split:
                paragraph = paragraph.strip()
                # substitute single spaces for everything
                paragraph = re.sub(r'\s+', r' ', paragraph)
                if paragraph:
                    # write the paragraph 
                    p = doc.add_paragraph()
                    p.style = 'Indent'
                    run = p.add_run(paragraph)
                    font = run.font
                    font.name = core.settings["font"]
                    font.size = Pt(int(core.settings["fontsize"]))

            return count
    else:
        print("ERROR: can't find scene file: " + scenefile)
        return 0

def write_chapter(doc, chapter, chapnum, chaptype="CHAPTER"):
    write_chapter_heading(doc, chapter, chapnum, chaptype)

    # write content
    first = True
    for scene in chapter["scenes"]:
        if not first:
            write_scene_separator(doc, scene)
        else:
            if core.settings["filescenesep"]:
                write_scene_separator(doc, scene)
            first = False

        if not scene.endswith(".pdf"):
            write_scene(doc, scene)

def write_chapters(doc, manuscript):
    chapnum = 1

    for chapter in manuscript["chapters"]:
        if core.check_chapter_tags(chapter, core.settings["tags"]):
            if core.is_prologue(chapter) or core.is_epilogue(chapter):
                chaptype = chapter["type"].upper()
                if core.settings["chaptersummary"]:
                    write_chaptersummary(f, chapter, chapnum, chaptype)
                else:
                    write_chapter(f, chapter, chapnum, chaptype)
            else:
                if core.settings["chaptersummary"]:
                    write_chaptersummary(f, chapter, chapnum)
                else:
                    write_chapter(doc, chapter, chapnum)
                chapnum += 1


def write(outputfile):

    with open( outputfile, "w") as f:
        success = True

        # create the one document
        theDocument  = Document()

        # construct the document
        write_preamble(theDocument)
        write_docinfo(theDocument)
        # write_headers(theDocument)
        write_title(theDocument)
        add_section(theDocument, WD_SECTION.CONTINUOUS)
        # debug_sections(theDocument)
        write_chapters(theDocument, core.manuscript)
        write_postamble(theDocument)

        theDocument.save(outputfile)

        if (success == True):
            print("wrote file: " + core.settings["outputfile"])



