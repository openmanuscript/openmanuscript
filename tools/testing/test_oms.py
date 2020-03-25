import unittest
import os
import filecmp
import shutil

class TestCIS(unittest.TestCase):

    def setUp(self):
        self.scratchdir = os.path.join("testing", "scratch")
        self.golddir    = os.path.join("testing", "gold")

    def tearDown(self):
        # clean up 
        shutil.rmtree( self.scratchdir )

    def test_oms(self):
        msdir  = "../example"
        msfile = "manuscript.json"
        afile  = "author.json"

        # make a testing area
        os.mkdir(self.scratchdir)
        
        # export docx
        ofile  = os.path.join(self.scratchdir, "omstest_manuscript.docx")
        print("Running oms")
        os.system("./oms --manuscriptdir {} --manuscriptfile {} --authorfile {} --outputfile {}".format(msdir, msfile, afile, ofile))

        # export docx
        ofile  = os.path.join(self.scratchdir, "omstest_manuscript_noquote-nosynopsis.docx")
        print("Running oms")
        os.system("./oms --exclude_tags quote synopsis --manuscriptdir {} --manuscriptfile {} --authorfile {} --outputfile {}".format(msdir, msfile, afile, ofile))
        
        # export docx
        ofile  = os.path.join(self.scratchdir, "omstest_manuscript_simple.docx")
        print("Running oms")
        os.system("./oms --include_tags simple --exclude_tags quote synopsis --manuscriptdir {} --manuscriptfile {} --authorfile {} --outputfile {}".format(msdir, msfile, afile, ofile))
        
        # export docx
        ofile  = os.path.join(self.scratchdir, "omstest_manuscript_notes.docx")
        print("Running oms")
        os.system("./oms --notes --manuscriptdir {} --manuscriptfile {} --authorfile {} --outputfile {}".format(msdir, msfile, afile, ofile))
        
        # export outline
        basefile = "omstest_manuscript_outline.html"
        ofile = os.path.join(self.scratchdir, basefile) 
        ofile_gold = os.path.join(self.golddir, basefile) 
        print("Running oms2outline")
        os.system("./oms2outline --manuscriptdir {} --manuscriptfile {} --authorfile {} --outputfile {}".format(msdir, msfile, afile, ofile))
        self.assertTrue( filecmp.cmp(ofile, ofile_gold), 'outline files differ')

