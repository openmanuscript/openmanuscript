import unittest
import os
import filecmp
import shutil
import openms

class TestCIS(unittest.TestCase):

    def setUp(self):
        self.scratchdir = os.path.join("testing", "scratch") 
        self.golddir    = os.path.join("testing", "gold")

    def tearDown(self):
        # clean up 
        clean = False
        if clean:
            shutil.rmtree( self.scratchdir )
        else:
            print("Not cleaning up from test ...")

    def test_oms(self):
        msdir  = "../example"
        msfile = "manuscript.json"
        afile  = "author.json"
        sfile  = "draft.json"
        extest = ["summary endnotes", "excludetext"]

        # make a testing area
        os.mkdir(self.scratchdir)
        
        # export docx
        ofile  = os.path.join(self.scratchdir, "omstest_manuscript.docx")
        print("Running oms for base test")
        os.system("./oms --manuscriptdir {} --manuscriptfile {} --authorfile {} --outputfile {}".format(msdir, msfile, afile, ofile))
        # can't perform test: files with equivalent content show as different

        # export docx with settings file, additional command line argument and 
        # command line argument override
        ofile  = os.path.join(self.scratchdir, "omstest_settings.docx")
        print("Running oms for settings file test")
        os.system("./oms --settingsfile {}/{} --manuscriptdir {} --outputfile {}".format(msdir, sfile, msdir, ofile))
        # can't perform test: files with equivalent content show as different

        # export docx
        ofile  = os.path.join(self.scratchdir, "omstest_manuscript_noquote-nosynopsis.docx")
        print("Running oms for no quote no synopsis")
        os.system("./oms --excludetags quote synopsis --manuscriptdir {} --manuscriptfile {} --authorfile {} --outputfile {}".format(msdir, msfile, afile, ofile))
        # can't perform test: files with equivalent content show as different
        
        # export docx
        ofile  = os.path.join(self.scratchdir, "omstest_manuscript_simple.docx")
        print("Running oms for simple test")
        os.system("./oms --includetags simple --excludetags quote synopsis --manuscriptdir {} --manuscriptfile {} --authorfile {} --outputfile {}".format(msdir, msfile, afile, ofile))
        # can't perform test: files with equivalent content show as different
        
        # export docx
        ofile  = os.path.join(self.scratchdir, "omstest_manuscript_notes.docx")
        print("Running oms for notes")
        os.system("./oms --notes --manuscriptdir {} --manuscriptfile {} --authorfile {} --outputfile {}".format(msdir, msfile, afile, ofile))
        # can't perform test: files with equivalent content show as different

        # export docx
            # don't exclude
        basefile = "omstest_manuscript_dont-exclude.docx"
        ofile = os.path.join(self.scratchdir, basefile) 
        ofile_gold = os.path.join(self.golddir, basefile) 
        emsfile = "exclude.json"
        print("Running oms for exclude check (don't exclude)")
        os.system("./oms --notes --manuscriptdir {} --manuscriptfile {} \
                        --authorfile {} --outputfile {} --excludesections {} --includesections {}".format(
                         msdir, emsfile, afile, ofile, extest[1], extest[0]))
            # exclude
        ofile = os.path.join(self.scratchdir, "omstest_manuscript_exclude.docx")
        print("Running oms for exclude check (exclude)")
        os.system("./oms --notes --manuscriptdir {} --manuscriptfile {} \
                        --authorfile {} --outputfile {} --excludesections {} --includesections {}".format(
                         msdir, emsfile, afile, ofile, extest[0], extest[1]))
        # can't perform test: files with equivalent content show as different
        # self.assertTrue( filecmp.cmp(ofile, ofile_gold), 'exclude files differ')

        # export outline
        basefile = "omstest_manuscript_outline.html"
        ofile = os.path.join(self.scratchdir, basefile) 
        ofile_gold = os.path.join(self.golddir, basefile) 
        print("Running oms2outline")
        os.system("./oms2outline --manuscriptdir {} --manuscriptfile {} --authorfile {} --outputfile {}".format(msdir, msfile, afile, ofile))
        self.assertTrue( filecmp.cmp(ofile, ofile_gold), 'outline files differ')

        # export outline
        basefile = "omstest_manuscript_outline_settings.html"
        ofile = os.path.join(self.scratchdir, basefile) 
        # ofile_gold is the same as the one for the test above
        print("Running oms2outline with settings file")
        os.system("./oms2outline --settingsfile {}/{} --manuscriptdir {} --manuscriptfile {} --outputfile {}".format(msdir, sfile, msdir, msfile, ofile))
        self.assertTrue( filecmp.cmp(ofile, ofile_gold), 'outline files differ')

        # test template 
        testdir = os.path.join(self.scratchdir, "template")
        os.mkdir(testdir)
        openms.template.write_template(testdir)

        # test short story 
        basefile = "omstest_manuscript_shortstory.docx"
        ofile  = os.path.join(self.scratchdir, basefile) 
        ofile_gold = os.path.join(self.golddir, basefile) 
        print("Running oms for short story")
        msfile = "short.json"
        os.system("./oms --manuscripttype story --notes --manuscriptdir {} --manuscriptfile {} --authorfile {} --outputfile {}".format(msdir, msfile, afile, ofile))
        # can't perform test: files with equivalent content show as different
        # self.assertTrue( filecmp.cmp(ofile, ofile_gold), 'short story files differ')
