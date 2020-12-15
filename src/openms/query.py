from . import core

import yaml
import json
import sys
import argparse
import textwrap
import os

def print_chapter(c):
    print("")
    print(c["title"])
    if "scenes" in c:
        print(c["scenes"])
    print("")
    if "desc" in c:
        print(c["desc"])

def execute(args):

    # load defaults
    # NOTE: this is not the same way it's done other places. 
    #       should standardize this
    defaults = {
        "settingsfile": "./.oms/query.yaml"
    }
    if os.path.isfile(defaults["settingsfile"]):
        with open( defaults["settingsfile"] ) as minputs:
            defaults = yaml.load( minputs, Loader=yaml.FullLoader )

    # override settings from command line, if provided
    if args.excludetags != None:
        core.set("excludetags", args.excludetags)
    if args.includetags != None:
        core.set("includetags", args.includetags)
    if args.todo != None:
        core.set("todo", args.todo)


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
            if core.check_chapter_tags(chapter):
                print(chapter["title"])
                if "scenes" in chapter:
                    print("  {}".format(chapter["scenes"]))

    elif args.scenes != None:
        all_scenes = []
        for chapter in data["chapters"]:
            if "scenes" in chapter:
                all_scenes = all_scenes + chapter["scenes"]
        all_scenes.sort()        
        all_scenes = list(dict.fromkeys(all_scenes))
        print("{} scenes:".format(len(all_scenes)))
        print(all_scenes)

    elif args.chapter != None:
        for chapter in data["chapters"]:
            if args.chapter == chapter["title"]:
                print_chapter(chapter)

    elif args.state != None:
        found_state = False
        for chapter in data["chapters"]:
            if "state" in chapter:
                if chapter["state"] == args.state: 
                    print_chapter(chapter)
                    found_state = True

        if not found_state:
            print("No chapter with state {} found".format(args.state))

    elif args.tag != None:
        found_tag = False
        for chapter in data["chapters"]:
            if "tags" in chapter:
                if args.tag in chapter["tags"]:
                    print_chapter(chapter)
                    found_state = True

        if not found_tag:
            print("No chapter with tag {} found".format(args.tag))

    if args.todo != None:
        print("")
        print("{}".format(data["title"]))
        print("")
        for chapter in data["chapters"]:
            if core.check_chapter_tags(chapter):
                print("{}".format(chapter["title"]))
                if "todo" in chapter:
                    for item in chapter["todo"]:
                        print("  - {}".format(item))



