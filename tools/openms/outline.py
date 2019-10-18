# ---------------------------------------------------------------------------
#
# html.py, an html conversion module for the OpenManuscript toolset 
#
# ---------------------------------------------------------------------------
"""
Copyright (c) 2016-2019, David H. Rogers 
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from . import core

import json
import os
import re
import datetime


# ---------------------------------------------------------------------------
# global variables
# ---------------------------------------------------------------------------
APP = {
    "name"      : "oms2html",
    "version"   : "1.0"
}

#
# current state
#   listnum - current number for numbered lists
#
CURSTATE = {
}

FONT = {
}

OUTLINE_COL_WIDTHS = {
    'title': '5', 
    'arc' : '5',
    'tod': '5', 
    'pov': '5', 
    'setting': '5', 
    'scenes': '5', 
    'desc': '30', 
    'story': '40'
}

OUTLINE_CSS = """
table {
    border: 1px solid black;
    background: grey;
    font-size: small;
}

th {
    background: lightgrey;
    vertical-align: top;
    font-size: small;
}

td {
    background: white;
    vertical-align: top;
    padding: 5px 5px 5px 5px;
    font-size: small;
}
"""

# -----------------------------------------------------------------------------
# write document preamble
# -----------------------------------------------------------------------------
def write_preamble( f, manuscript ):
    f.write("<html>\n")
    f.write("<html>\n")
    f.write("<head>\n")
    f.write("<title>{}</title>\n".format(manuscript["title"]))
    f.write("<style>{}</style>\n".format(OUTLINE_CSS))
    f.write("</head>\n")
    f.write("<body>\n")

# -----------------------------------------------------------------------------
# write the title
# -----------------------------------------------------------------------------
def write_title(f, manuscript, author):
    f.write("<h2>{}</h2>\n".format(manuscript["title"]))
    if "desc" in manuscript:
        f.write("<p><strong>Description:</strong>&nbsp{}\n</p>\n".format(manuscript["desc"]))

# -----------------------------------------------------------------------------
# finish things up and make a valid document
# -----------------------------------------------------------------------------
def write_postamble(f):
    f.write("</body>\n</html>")
    f.write("</html>\n</html>")

# -----------------------------------------------------------------------------
# under certain conditions, substitute underlines for bold 
# -----------------------------------------------------------------------------
def sub_bold( data ):
    if core.settings["underline"]:
        data  = re.sub(r'\*\*([^*]+)\*\*', r'<u>\1</u>', data)
    else:
        data  = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', data)
    return data

# -----------------------------------------------------------------------------
# under certain conditions, substitute underlines for italics 
# -----------------------------------------------------------------------------
def sub_italics( data ):
    if core.settings["underline"]:
        data  = re.sub(r'\*\*([^*]+)\*\*', r'<u>\1</u>', data)
    else:
        data  = re.sub(r'\*\*([^*]+)\*\*', r'<em>\1</em>', data)

    return data

# -----------------------------------------------------------------------------
#
# write this object's data into an html file 
#
# -----------------------------------------------------------------------------
def write_outline():
    result = False
    with open( core.settings["outputfile"], "w" ) as f:
        result = True
        chapnum = 1;
        write_preamble(f, core.manuscript)
        # header
        f.write("<h3>{} Outline</h3>\n".format(core.manuscript["title"]))

        # table of chapters
        f.write("<table>\n")
        f.write("<tr>\n")
        f.write("<th style=\"width:1%\">Chapter</th>\n")
        for col in core.settings["columns"]:
            f.write("<th style=\"width:{0}%\">{1}</th>".
                format(OUTLINE_COL_WIDTHS[col.lower()], col))
        f.write("</tr>\n")
        tags = None
        for chapter in core.manuscript["chapters"]:
            if (core.check_chapter_tags( chapter, tags )):
                f.write("<tr>\n")
                f.write("<td>{0}</td>\n".format(chapnum))
                chapnum = chapnum + 1
                for col in core.settings["columns"]:
                    if (col.lower() in chapter):
                        if (col == "Scenes"):
                            f.write("<td>")
                            for scene in chapter[col.lower()]:
                                f.write("<a href=\"../scenes/{}.md\">{}</a>&nbsp\n".format(scene, scene))
                            f.write("</td>\n")
                            # f.write("<td>{0}</td>\n".format(" ".join(chapter[col.lower()])))
                        else:
                            f.write("<td>{0}</td>\n".
                                format(chapter[col.lower()]))
                    else:
                        f.write("<td></td>\n")
                f.write("</tr>\n")

        f.write("</table>\n")
        write_postamble(f)

    return result

