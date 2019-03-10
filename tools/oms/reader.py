import os
import json
from .oms import *

reader = {
    "oms" : "none",
    "authorfile" : "none",
    "manuscriptfile" : "none",
    "manuscriptdir"  : "none"
}

author = {
}

manuscript = {
}

def check_version( json_data ):
    result = 0

    if "version" in json_data:
        if json_data["version"] == OMS["version"]:
            result = 1
        else:
            print("ERROR: unsupported openmanuscript version: {}"
                    .format(json_data["version"]))
    else:
        print("ERROR: invalid json data (no version number)") 

    return result

def set_manuscriptdir( msdir ):
    global reader
    reader["manuscriptdir"] = msdir

def set_manuscriptfile( mfile ):
    global reader
    reader["manuscriptfile"] = mfile 

def set_authorfile( afile ):
    global reader
    reader["authorfile"] = afile 

def get_authorfile():
    global reader
    return os.path.join( reader["manuscriptdir"], reader["authorfile"] )

def get_manuscriptfile():
    global reader
    return os.path.join( reader["manuscriptdir"], reader["manuscriptfile"] )

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
        
