import os
import json
import csv
import re
import glob

__oms = {
    "name"        : "OpenManuscript",
    "toolversion" : "2.2",
    "specversion" : "2.0"
}

settings = {
    "authorfile"      : "author.json",
    "chaptersummary"  : False,
    "columns"         : None,
    "exclude_tags"    : None, 
    "filescenesep"    : False,
    "font"            : "Courier",
    "fontsize"        : "12",
    "include_tags"    : None, 
    "includesettings" : None, 
    "notes"           : False,
    "manuscriptdir"   : ".",
    "manuscriptfile"  : "manuscript.json",
    "outputfile"      : "manuscript.rtf"
}

author = {
}

manuscript = {
}

def get_next_scene(dir):
    next_scene = "000"

    globstring = '{}/[0-9]*.md'.format( os.path.join(dir) )
    scenes = glob.glob( globstring )
    if len(scenes) != 0:
        scenes.sort()
        next_scene = os.path.basename(scenes[-1])
        next_scene = os.path.splitext(next_scene)[0] 
        next_scene = int(next_scene)
        next_scene += 1
        next_scene = "{:03}.md".format(next_scene)

    return next_scene
    

def set(attribute, value):
    global settings
    settings[attribute] = value

def set_manuscriptdir( msdir ):
    global settings
    settings["manuscriptdir"] = msdir

def set_manuscriptfile( mfile ):
    global settings
    settings["manuscriptfile"] = mfile 

def set_authorfile( afile ):
    global settings
    settings["authorfile"] = afile 

def get_name():
    global __oms
    return __oms["name"]

def get_version():
    return get_tool_version()

def get_tool_version():
    global __oms
    return __oms["toolversion"]

def get_spec_version():
    global __oms
    return __oms["specversion"]

def get_authorfile():
    global settings
    return os.path.join( settings["manuscriptdir"], settings["authorfile"] )

def get_manuscriptfile():
    global settings
    return os.path.join( settings["manuscriptdir"], settings["manuscriptfile"] )

def get_author():
    global author
    return author

def get_manuscript():
    global manuscript
    return manuscript

def get_scenefile( scene ):
    global settings
    # make sure it has the correct ending
    scene = clean_scene_filename(scene)
    return os.path.join( settings["manuscriptdir"], "scenes", scene)

def get_output_type():
    name, ext = os.path.splitext(settings["outputfile"])
    ext, numtimes = re.subn(r'^.', r'', ext)
    return ext

def get_chapter_type(chapter):
    chaptype = None
    if "type" in chapter:
        chaptype = chapter["type"].upper()
    else:
        chaptype = "CHAPTER"

    return chaptype


# ---------------------------------------------------------------------------
# clean scene filename 
#
# ensure that the scene filename ends in .md, whether it has it already
# or not
# ---------------------------------------------------------------------------
def clean_scene_filename(scene): 
    if scene.endswith(".md"):
        return scene
    else:
        return scene + ".md"

# ---------------------------------------------------------------------------
# check tags in a chapter against those requested to be included
# ---------------------------------------------------------------------------
def check_chapter_tags( chapter ): 
    include = True
    exclude = False

    if (not ("tags" in chapter)):
        if (settings["include_tags"] != None):
            include = False 
        else:
            include = True

        exclude = False
    else:
        if (settings["include_tags"] != None):
            include = any( i in chapter["tags"] for i in settings["include_tags"])
        else:
            include = True

        if (settings["exclude_tags"] != None):
            exclude = any( i in chapter["tags"] for i in settings["exclude_tags"])
        else:
            exclude = False

    results = True
    if (include and not exclude):
        result = True
    else:
        result = False

    return result

# ---------------------------------------------------------------------------
# check type of a chapter 
# ---------------------------------------------------------------------------
def check_chapter_type( chapter, chaptype ): 
    result = False

    if (not chaptype is None) and (("type" in chapter) and 
        (chaptype in chapter["type"])):
        result = True

    return result

# -----------------------------------------------------------------------------
# check for a prologue 
# -----------------------------------------------------------------------------
def is_prologue( chapter ):
    return check_chapter_type( chapter, "prologue" ) 

# -----------------------------------------------------------------------------
# check for an epilogue 
# -----------------------------------------------------------------------------
def is_epilogue( chapter ):
    return check_chapter_type( chapter, "epilogue" ) 

# -----------------------------------------------------------------------------
# format horizontal rule
# -----------------------------------------------------------------------------
def is_horrule( data ):
    (junk, num) = re.subn(r'^(---|###|\*\*\*)', r'HERE', data)

    return num 

# -----------------------------------------------------------------------------
# format bulleted lists 
# -----------------------------------------------------------------------------
def is_bulletlist_item( data ):
    (junk, num) = re.subn(r'^\s*\-', r'HERE', data)

    return num 

# -----------------------------------------------------------------------------
# format numbered lists 
# -----------------------------------------------------------------------------
def is_numberedlist_item( data ):
    (junk, num) = re.subn(r'^\s*[0-9]+\.', r'HERE', data)

    return num 

# -----------------------------------------------------------------------------
# format headers 
# -----------------------------------------------------------------------------
def is_header( data ):
    (junk, num) = re.subn(r'^\s*\#+\s', r'HERE', data)

    return num 

def check_version( json_data ):
    global __oms

    result = 0

    if "version" in json_data:
        if json_data["version"] == __oms["specversion"]:
            result = 1
        else:
            print("ERROR: unsupported openmanuscript version: {}"
                    .format(json_data["version"]))
    else:
        print("ERROR: invalid json data (no version number)") 

    return result


def read_data():
    global author
    global manuscript

    with open( get_authorfile() ) as author_file:
        author = json.load( author_file )
        if (check_version(author)):
            author = author["author"]

    with open( get_manuscriptfile() ) as manuscript_file:
        manuscript = json.load( manuscript_file )
        if (check_version(manuscript)):
            manuscript = manuscript["manuscript"]
        

def csv_to_manuscript( csvfile, ms ):
    with open(csvfile, "r") as csvdata:
        csvreader = csv.reader(csvdata, delimiter=',')

        with open(ms, "w") as mfile:

            mfile.write("{\n")
            mfile.write("\"version\" : \"{}\",\n".format(get_version()))
            mfile.write("\"manuscript\" : {\n")
            mfile.write("    \"title\" : \"Sample\",\n")
            mfile.write("    \"runningtitle\" : \"sample\",\n")
            mfile.write("    \"chapters\" : [\n")

            count = 0
            first = 1
            for row in csvreader:
                if (count > 1):
                    mfile.write(",\n")

                if (count == 0):
                    names = row.copy()
                else:
                    values = row.copy()

                    mfile.write("         {\n")
                    for i in range(len(names)): 
                        mfile.write("             \"{}\" : \"{}\"".format(names[i].strip(), values[i].strip()))
                        if (i == (len(names)-1)):
                            mfile.write("\n")
                        else:
                            mfile.write(",\n")
                if (count != 0):
                    mfile.write("         }")
                count += 1 

            mfile.write("\n")
            mfile.write("    ]\n")
            mfile.write("}\n")
            mfile.write("}\n")



def manuscript_to_csv( mdir, mfile, afile, ofile ):
    global manuscript

    set_manuscriptdir(mdir)
    set_manuscriptfile(mfile)
    set_authorfile(afile)
    read_data()

    names = ["title", "pov", "tod", "setting", "desc"]

    with open(ofile, "w") as ofile:
        first = True
        for name in names:
            if first:
                first = False
            else:
                ofile.write(",")
            ofile.write(name)

        ofile.write("\n")

        for chapter in manuscript["chapters"]:
            first = True
            for name in names:
                if first:
                    first = False
                else:
                    ofile.write(",")
                if name in chapter:  
                    value = chapter[name]
                else:
                    value = ""
                ofile.write("\"{}\"".format(value))

            ofile.write("\n")

def manuscript_to_html( mdir, mfile, afile, ofile ):
    global manuscript

    set_manuscriptdir(mdir)
    set_manuscriptfile(mfile)
    set_authorfile(afile)
    read_data()

    with open( get_authorfile() ) as author_file:
        author = json.load( author_file )
        if (check_version(author)):
            author = author["author"]

    with open(ofile, "w") as ofile:
        ofile.write("<html>")
        ofile.write("<title>{}</title>\n".format(manuscript["title"]))
        ofile.write("<head>")
        ofile.write("</head>")
        ofile.write("<body>")
        ofile.write("<h2><strong>{}</strong></h2>\n".format(manuscript["title"]))
        for chapter in manuscript["chapters"]:
            ofile.write("<p>")
            ofile.write("<strong>{}</strong>\n".format(chapter["title"]))
            ofile.write("<ul>")
            for scene in chapter["scenes"]:
                ofile.write("<li>{}</li>".format(scene))
            ofile.write("</ul>")
            ofile.write("</p>")
        ofile.write("</body>")
        ofile.write("</html>")

def get_scenelist():
    global manuscript

    read_data()

    scenelist = []
    for chapter in manuscript["chapters"]:
        for scene in chapter["scenes"]:
            scenelist.append(scene)

    newlist = []
    for i in scenelist:
        if i not in newlist:
            newlist.append(i)
    newlist.sort()

    return newlist 

def find_tagged_scenes():
    scenes = []

    for chapter in manuscript["chapters"]:
        if check_chapter_tags( chapter ):
            scenes.extend(chapter["scenes"])

    return scenes

def get_word_count( fname ):
    count = 0

    with open( fname ) as scenefile:
        for line in scenefile:
            count += len(line.split()) 

    return count

def get_approximate_word_count():
    scenes = find_tagged_scenes()

    count = 0
    for scene in scenes:
        count = count + get_word_count(get_scenefile(scene))

    count -= count % -100 
    return count
