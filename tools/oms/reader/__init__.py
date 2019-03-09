import os
import json

READER = {
    "oms" : "none",
    "authorfile" : "none",
    "manuscriptfile" : "none"
}

AUTHOR = {
}

MANUSCRIPT = {
}

def set_database( db ):
    global READER

    READER["db"] = db
    READER["authorfile"] = os.path.join( db, "author.json" )
    READER["manuscriptfile"] = os.path.join( db, "manuscript.json" )

def get_authorfile():
    return READER["authorfile"]

def get_manuscriptfile():
    return READER["manuscriptfile"]

def get_author():
    global AUTHOR
    return AUTHOR

def get_manuscript():
    global MANUSCRIPT
    return MANUSCRIPT

def read():
    global AUTHOR
    global MANUSCRIPT
    
    with open( get_authorfile() ) as author_file:
        AUTHOR = json.load( author_file )
        AUTHOR = AUTHOR["author"]

    with open( get_manuscriptfile() ) as manuscript_file:
        MANUSCRIPT = json.load( manuscript_file )
        MANUSCRIPT = MANUSCRIPT["manuscript"]
        
