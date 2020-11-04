import os

def write_template(path):
    write_authorfile(path)
    write_manuscriptfile(path)
    write_scenes(path)
    write_settingsfile(path)

def write_settingsfile(path):
    with open(os.path.join(path, "settings.json"), "w") as sfile:
        contents = """
{
    "manuscriptfile" : "manuscript.yaml",
    "toc"            : true
}
"""
        sfile.write(contents)

def write_authorfile(path):
    with open(os.path.join(path, "author.json"), "w") as afile:
        contents = """
{
"version" : "2.1",
"author" : {
    "name"      : "Ima Q. Writer (json)",
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
    with open(os.path.join(path, "author.yaml"), "w") as afile:
        contents = """
version : "2.1"
author :
    name      : Ima Q. Writer (yaml)
    surname   : Writer
    email     : imaqwriter@imawriter.com
    phone     : (000) 000-0000
    website   : www.imawriter.com
    streetAddress     : 111 Writer's Way
    addressLocality   : Writerville
    addressRegion     : NM
    addressCountry    : USA
    postalCode        : "88888"
"""
        afile.write(contents)

def write_manuscriptfile(path):
    with open(os.path.join(path, "manuscript.json"), "w") as mfile:
        contents = """
{
"version" : "2.1",
"manuscript" : {
    "title" : "OpenManuscript Template (json)",
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
    with open(os.path.join(path, "manuscript.yaml"), "w") as mfile:
        contents = """
version : "2.1"
manuscript :
    title : OpenManuscript Template (yaml)
    runningtitle : template
    chapters :
        -
            title   : The Big Beginning 
            pov     : Bill 
            scenes  : ["001", "002", "003"] 
            setting : The cabin
            story   : We are introduced to the main character
            tags    : ["final"] 
            tod     : night 
            desc    : |+
                The first chapter.
        -
            scenes  : [anything]
"""
        mfile.write(contents)

def write_scenes(path):
    scene_001 = """
This chapter shows how to string together a few scene files, and include the
full set of defined tags in a scene. In case your tools can take advantage of
the information, you can define things like **pov**, **setting**, etc. in the
**manuscript.json** file if you'd like.
"""
    scene_002 = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer nec odio. Praesent libero. Sed cursus ante dapibus diam. Sed nisi. Nulla quis sem at nibh elementum imperdiet. Duis sagittis ipsum. Praesent mauris. Fusce nec tellus sed augue semper porta. Mauris massa. Vestibulum lacinia arcu eget nulla. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Curabitur sodales ligula in libero. 

Sed dignissim lacinia nunc. Curabitur tortor. Pellentesque nibh. Aenean quam. In scelerisque sem at dolor. Maecenas mattis. Sed convallis tristique sem. Proin ut ligula vel nunc egestas porttitor. Morbi lectus risus, iaculis vel, suscipit quis, luctus non, massa. Fusce ac turpis quis ligula lacinia aliquet. Mauris ipsum. 

Nulla metus metus, ullamcorper vel, tincidunt sed, euismod in, nibh. Quisque volutpat condimentum velit. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Nam nec ante. Sed lacinia, urna non tincidunt mattis, tortor neque adipiscing diam, a cursus ipsum ante quis turpis. Nulla facilisi. Ut fringilla. Suspendisse potenti. Nunc feugiat mi a tellus consequat imperdiet. Vestibulum sapien. Proin quam. Etiam ultrices. Suspendisse in justo eu magna luctus suscipit. 

Sed lectus. Integer euismod lacus luctus magna. Quisque cursus, metus vitae pharetra auctor, sem massa mattis sem, at interdum magna augue eget diam. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Morbi lacinia molestie dui. Praesent blandit dolor. Sed non quam. In vel mi sit amet augue congue elementum. Morbi in ipsum sit amet pede facilisis laoreet. Donec lacus nunc, viverra nec, blandit vel, egestas et, augue. Vestibulum tincidunt malesuada tellus. Ut ultrices ultrices enim. Curabitur sit amet mauris. Morbi in dui quis est pulvinar ullamcorper. 

Nulla facilisi. Integer lacinia sollicitudin massa. Cras metus. Sed aliquet risus a tortor. Integer id quam. Morbi mi. Quisque nisl felis, venenatis tristique, dignissim in, ultrices sit amet, augue. Proin sodales libero eget ante. Nulla quam. Aenean laoreet. Vestibulum nisi lectus, commodo ac, facilisis ac, ultricies eu, pede. Ut orci risus, accumsan porttitor, cursus quis, aliquet eget, justo. Sed pretium blandit orci. 
"""
    scene_003 = scene_002
    scene_anything = """
This example shows the minimum you need to describe a manuscript. It's basically
just a list of chapters, each of which is a list of scenes.

You'll notice in the **manuscript.json** file that this chapter only has one 
thing defined: the **scenes** fields. Everything else is optional, because 
**OpenManuscript** tools are required to behave well when information isn't defined.

Also, just remember that the name of the scene file is up to you - numbering
them in order makes it easy to create unique names, but you can name them
anything you want.
"""
    scenepath = os.path.join(path, "scenes")
    os.mkdir(scenepath)
    with open(os.path.join(scenepath, "001.md"), "w") as sfile:
        sfile.write(scene_001)
    with open(os.path.join(scenepath, "002.md"), "w") as sfile:
        sfile.write(scene_002)
    with open(os.path.join(scenepath, "003.md"), "w") as sfile:
        sfile.write(scene_002)
    with open(os.path.join(scenepath, "anything.md"), "w") as sfile:
        sfile.write(scene_anything)
