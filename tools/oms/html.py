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

# -----------------------------------------------------------------------------
# write document preamble
# -----------------------------------------------------------------------------
def write_preamble( f ):
    f.write("<html>\n")

# -----------------------------------------------------------------------------
# write the title
# -----------------------------------------------------------------------------
def write_title(f, manuscript, author):
    f.write("<head>\n<title>{}</title>\n</head>\n".format(manuscript["title"]))
    f.write("<body>\n<h2>{}</h2>\n".format(manuscript["title"]))
    if "desc" in manuscript:
        f.write("<p><strong>Description:</strong>&nbsp{}\n</p>\n".format(manuscript["desc"]))

# -----------------------------------------------------------------------------
# finish things up and make a valid document
# -----------------------------------------------------------------------------
def write_postamble(f):
    f.write("</body>\n</html>")

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
def write( ofile ):

    with open( ofile, "w" ) as f:
        success = True

        write_preamble(f)
        write_title(f, core.manuscript, core.author)
        for chapter in core.manuscript["chapters"]:
            f.write("<p><strong>{}</strong>&nbsp&nbsp&nbsp&nbsp".format(chapter["title"]))
            if "desc" in chapter:
                f.write("{}\n".format(chapter["desc"]))
            f.write("</p>\n")

            f.write("<ul>\n")
            for scene in chapter["scenes"]:
                f.write("<li><a href=\"scenes/{}.md\">{}</li></a>\n".format(scene, scene))
            f.write("</ul>\n")
        write_postamble(f)
