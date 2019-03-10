import os
import json
from .oms import *

settings = {
    "authorfile" : "author.json",
    "manuscriptfile" : "manuscript.json",
    "manuscriptdir"  : "none"
}

author = {
}

manuscript = {
}

def check_version( json_data ):
    result = 0

    if "version" in json_data:
        if json_data["version"] == OMS["specversion"]:
            result = 1
        else:
            print("ERROR: unsupported openmanuscript version: {}"
                    .format(json_data["version"]))
    else:
        print("ERROR: invalid json data (no version number)") 

    return result

def set_manuscriptdir( msdir ):
    global settings
    settings["manuscriptdir"] = msdir

def set_manuscriptfile( mfile ):
    global settings
    settings["manuscriptfile"] = mfile 

def set_authorfile( afile ):
    global settings
    settings["authorfile"] = afile 

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

def read():
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
        
