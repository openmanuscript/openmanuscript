import yaml
import json
import sys
import argparse
import textwrap
import os

desc = """A tool that queries OpenManuscript databases 
"""
ep = """
Examples:
    omsquery --chapters
        Prints all chapter names in the default manuscript.

    omsquery --chapter <chapter name>
        Prints the chapter information about the named chapter 

    omsquery --manuscriptfile name.yaml --chapters
        Prints all chapter names in the named manuscript.

    omsquery --manuscriptfile name.yaml --current
        Prints the chapter information about the current chapter (state) 

"""
parser = argparse.ArgumentParser(
                    formatter_class=argparse.RawDescriptionHelpFormatter,
                    description=textwrap.dedent(desc),
                    epilog=textwrap.dedent(ep)
                    )

parser.add_argument( "--manuscriptfile", default=None,
    help="Read manuscript definition from this file.")
parser.add_argument( "--chapters", action="store_true", default=None,
    help="Print the chapter names in the manuscript file")
parser.add_argument( "--chapter", default=None,
    help="Chapter name for this operation")
parser.add_argument( "--current", action="store_true", default=None,
    help="Find the current chapter for this operation")
parser.add_argument( "--scenes", action="store_true", default=None,
    help="Print the set of scenes in the manuscript file")

args, remaining_argv = parser.parse_known_args()

#
# define some functions
#
def print_chapter(c):
    print("")
    print(c["title"])
    print(c["scenes"])
    print("")
    if "desc" in c:
        print(c["desc"])


#
# execute
#

# load defaults
defaults = {
    "settingsfile": "./.oms/query.yaml"
}
if os.path.isfile(defaults["settingsfile"]):
    with open( defaults["settingsfile"] ) as minputs:
        defaults = yaml.load( minputs, Loader=yaml.FullLoader )

if args.manuscriptfile == None:
    if "manuscriptfile" in defaults:
        args.manuscriptfile = defaults["manuscriptfile"] 
    else:
        print("ERROR: must provide manuscriptfile")
        exit(0)

data = None
with open( args.manuscriptfile ) as infile:
    if args.manuscriptfile.endswith( "json" ):
        data = json.load( infile )
    elif args.manuscriptfile.endswith( "yaml" ):
        data = yaml.load( infile, Loader=yaml.FullLoader ) 

data = data["manuscript"]

if args.chapters != None:
    for chapter in data["chapters"]:
        print(chapter["title"])

elif args.scenes != None:
    all_scenes = []
    for chapter in data["chapters"]:
        all_scenes = all_scenes + chapter["scenes"]
    all_scenes.sort()        
    all_scenes = list(dict.fromkeys(all_scenes))
    print("{} scenes:".format(len(all_scenes)))
    print(all_scenes)

elif args.chapter != None:
    for chapter in data["chapters"]:
        if args.chapter == chapter["title"]:
            print_chapter(chapter)

elif args.current != None:
    found_current = False
    for chapter in data["chapters"]:
        if "state" in chapter:
            if chapter["state"] == "current":
                found_current = True
                print_chapter(chapter)

    if not found_current:
        print("No current chapter found")


    



