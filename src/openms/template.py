import os

def write_authorfile(path):
    with open(os.path.join(path, "author.json"), "w") as afile:
        contents = """
{
"version" : "2.0",
"author" : {
    "name"      : "Ima Q. Writer",
    "surname"   : "Writer",
    "email"     : "imaqwriter@imawriter.com",
    "phone"     : "(000) 000-0000",
    "website"   : "www.imawriter.com",
    "streetAddress"     : "111 Writer's Way",
    "addressLocality"   : "Writerville",
    "addressRegion"     : "NM",
    "addressCountry"    : "USA",
    "postalCode"        : "88888"
}
}
"""
        afile.write(contents)

def write_manuscriptfile(path):
    with open(os.path.join(path, "manuscript.json"), "w") as mfile:
        contents = """
{
"version" : "2.0",
"manuscript" : {
    "title" : "OpenManuscript Template",
    "runningtitle" : "template",
    "chapters" : [
        {
            "desc"    : "The first chapter", 
            "pov"     : "Bill", 
            "scenes"  : ["001", "002", "003"], 
            "setting" : "The cabin",
            "story"   : "We are introduced to the main character",
            "tags"    : ["final"], 
            "title"   : "The Big Beginning", 
            "tod"     : "night" 
        },
        {
            "scenes"  : ["anything"]
        }
    ]
}
}
"""
        mfile.write(contents)
