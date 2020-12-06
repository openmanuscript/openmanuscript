import argparse
import configparser
import os
import json
import textwrap
import openms


def execute(args):
    # set settings from a file, if provided 
    openms.core.set_settings_from_file(args.settingsfile)

    # override settings from command line, if provided
    if args.authorfile != None:
        openms.core.set("authorfile", args.authorfile)
    if args.chapterdesc != None:
        openms.core.set("chapterdesc", args.chapterdesc)
    if args.chaptersummary != None:
        openms.core.set("chaptersummary", args.chaptersummary)
    if args.excludesections != None:
        openms.core.set("excludesections", args.excludesections)
    if args.excludetags != None:
        openms.core.set("excludetags", args.excludetags)
    if args.filescenesep != None:
        openms.core.set("filescenesep", args.filescenesep)
    if args.font != None:
        openms.core.set("font", args.font)
    if args.fontsize != None:
        openms.core.set("fontsize", args.fontsize)
    if args.includesections != None:
        openms.core.set("includesections", args.includesections)
    if args.includetags != None:
        openms.core.set("includetags", args.includetags)
    if args.manuscriptdir != None:
        openms.core.set("manuscriptdir", args.manuscriptdir)
    if args.manuscriptfile != None:
        openms.core.set("manuscriptfile", args.manuscriptfile)
    if args.manuscripttype != None:
        openms.core.set("manuscripttype", args.manuscripttype)
    if args.notes != None:
        openms.core.set("notes", args.notes)
    if args.outputfile != None:
        openms.core.set("outputfile", args.outputfile)
    if args.slug != None:
        openms.core.set("slug", args.slug)
    if args.notitlepage != None:
        openms.core.set("notitlepage", args.notitlepage)
    if args.toc != None:
        openms.core.set("toc", args.toc)

    # ----------------------------------------------------------------------
    #
    # start to do stuff
    #
    # ----------------------------------------------------------------------

    if args.specversion:
        print(openms.core.get_spec_version())
        exit(0)

    if args.types:
        print("docx")
        exit(0)

    if args.newmanuscript != None:
        print("Creating new manuscript at {}".format(args.newmanuscript))
        if os.path.isdir(args.newmanuscript):
            print("ERROR: directory {} already exists".format(args.newmanuscript))
        else:
            os.mkdir(args.newmanuscript)
            if not os.path.isdir(args.newmanuscript):
                print("ERROR: can't create directory: {}".format(args.newmanuscript))
            else:
                openms.template.write_template(args.newmanuscript)
        exit(0)

    # check existence of the files we will need
    if not os.path.isfile(openms.core.get_authorfile()):
        print("ERROR: cannot open file: " + openms.core.get_authorfile())
        exit(1)

    if not os.path.isfile( openms.core.get_manuscriptfile() ):
        print("ERROR: cannot open file: " + openms.core.get_manuscriptfile())
        exit(1)

    # do everything
    if args.listscenes:
        scenes = openms.core.get_scenelist()
        for scene in scenes:
            print(scene)
        exit(0)

    output_type = openms.core.get_output_type()

    if (output_type == "docx"):
        openms.core.read_data()
        openms.docx.write( openms.core.get_setting("outputfile") )

    else:
        print("ERROR: cannot write output file of type \'{}\'".format(output_type))
        exit(1)


