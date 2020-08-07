import os
import json
import csv
import re
import glob
import yaml

__oms = {
    "name"        : "OpenManuscript",
    "toolversion" : "3.4",
    "specversion" : "2.0"
}

settings = {
    "authorfile"      : "author.json",
    "chapterdesc"     : False,
    "chaptersummary"  : False,
    "columns"         : ["Title", "Arc", "POV", "TOD", "Setting", "Scenes", "Desc"], 
    "excludesections" : None, 
    "excludetags"     : None, 
    "filescenesep"    : False,
    "font"            : "Courier",
    "fontsize"        : "12",
    "includesections" : None, 
    "includetags"     : None, 
    "manuscriptdir"   : ".",
    "manuscriptfile"  : "manuscript.json",
    "manuscripttype"  : "novel",
    "notes"           : False,
    "outputfile"      : "manuscript.docx",
    "toc"             : False
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
    
def get_setting(key):
    result = None
    if key in settings:
        result = settings[key]

    return result

def set(attribute, value):
    global settings
    # print("Setting: {}, {}".format( attribute, value))
    settings[attribute] = value

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
        if (settings["includetags"] != None):
            include = False 
        else:
            include = True

        exclude = False
    else:
        if (settings["includetags"] != None):
            include = any( i in chapter["tags"] for i in settings["includetags"])
        else:
            include = True

        if (settings["excludetags"] != None):
            exclude = any( i in chapter["tags"] for i in settings["excludetags"])
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

# -----------------------------------------------------------------------------
# check the version attribute of a data file 
# -----------------------------------------------------------------------------
def check_version( in_data ):
    global __oms

    result = False

    if "version" in in_data:
        if in_data["version"] == __oms["specversion"]:
            result = True
        else:
            print("ERROR: unsupported openmanuscript version: {}"
                    .format(in_data["version"]))
    else:
        print("ERROR: invalid data (no version number)") 

    return result

# -----------------------------------------------------------------------------
# load a data file, regardless of whether it is json or yaml
# report non-standard file types
# -----------------------------------------------------------------------------
def load_data_file( f, dtype="manuscript" ):
    data = None
    with open( f ) as infile:
        if f.endswith(".json"):
            data = json.load( infile )
        elif f.endswith(".yaml"):
            data = yaml.load( infile, Loader=yaml.FullLoader )
        else:
            print("ERROR: invalid data file type: {}".format(f))

    #
    # all data files have a version attribute that must be checked
    # if the attribute is valid, then the data is returned without
    # the verison information, from the next leve of the hierarchy 
    # this depends on the type of the data
    #
    if data is not None:
        if check_version(data):
            data = data[dtype]

    return data

def read_data():
    global author
    global manuscript

    afile = get_authorfile()
    author = load_data_file(afile, dtype="author")

    msfilename = get_manuscriptfile()
    manuscript = load_data_file(msfilename)

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

    set("manuscriptdir", mdir)
    set("manuscriptfile", mfile)
    set("authorfile", afile)
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

    set("manuscriptdir", mdir)
    set("manuscriptfile", mfile)
    set("authorfile", afile)
    read_data()

    afile = get_authorfile()
    author = load_data_file(afile, dtype="author")

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
