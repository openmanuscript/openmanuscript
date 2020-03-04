import unittest
import os
import filecmp
import shutil

class TestCIS(unittest.TestCase):

    def test_oms(self):
        msdir  = "../example"
        msfile = "manuscript.json"
        afile  = "author.json"
        scratchdir = os.path.join("testing", "scratch")
        golddir    = os.path.join("testing", "gold")

        # make a testing area
        os.mkdir(scratchdir)
        
        # export docx
        ofile  = os.path.join(scratchdir, "omstest_manuscript.docx")
        print("Running oms")
        os.system("./oms --manuscriptdir {} --manuscriptfile {} --authorfile {} --outputfile {}".format(msdir, msfile, afile, ofile))

        # export docx
        ofile  = os.path.join(scratchdir, "omstest_manuscript_noquote-nosynopsis.docx")
        print("Running oms")
        os.system("./oms --exclude_tags quote synopsis --manuscriptdir {} --manuscriptfile {} --authorfile {} --outputfile {}".format(msdir, msfile, afile, ofile))
        
        # export docx
        ofile  = os.path.join(scratchdir, "omstest_manuscript_simple.docx")
        print("Running oms")
        os.system("./oms --include_tags simple --exclude_tags quote synopsis --manuscriptdir {} --manuscriptfile {} --authorfile {} --outputfile {}".format(msdir, msfile, afile, ofile))
        
        # export docx
        ofile  = os.path.join(scratchdir, "omstest_manuscript_notes.docx")
        print("Running oms")
        os.system("./oms --notes --manuscriptdir {} --manuscriptfile {} --authorfile {} --outputfile {}".format(msdir, msfile, afile, ofile))
        
        # export outline
        basefile = "omstest_manuscript_outline.html"
        ofile = os.path.join(scratchdir, basefile) 
        ofile_gold = os.path.join(golddir, basefile) 
        print("Running oms2outline")
        os.system("./oms2outline --manuscriptdir {} --manuscriptfile {} --authorfile {} --outputfile {}".format(msdir, msfile, afile, ofile))
        self.assertTrue( filecmp.cmp(ofile, ofile_gold), 'outline files differ')

        # clean up 
        shutil.rmtree( scratchdir )
