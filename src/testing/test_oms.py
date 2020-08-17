import unittest
import os
import filecmp
import shutil
import openms
from subprocess import PIPE, Popen

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
        msfile_yaml = "manuscript.yaml"
        afile  = "author.json"
        afile_yaml  = "author.yaml"
        sfile  = "draft.json"
        extest = ["summary endnotes", "excludetext"]

        # make a testing area
        os.mkdir(self.scratchdir)
        
        # export docx
        ofile  = os.path.join(self.scratchdir, "omstest_manuscript.docx")
        print("Running oms for base test")
        os.system("./oms --manuscriptdir {} --manuscriptfile {} --authorfile {} --outputfile {}".format(msdir, msfile, afile, ofile))
        # can't perform test: files with equivalent content show as different

        # export docx
        ofile  = os.path.join(self.scratchdir, "omstest_manuscript_toc.docx")
        print("Running oms for base test with toc")
        os.system("./oms --manuscriptdir {} --manuscriptfile {} --authorfile {} --outputfile {} --toc".format(msdir, msfile, afile, ofile))
        # can't perform test: files with equivalent content show as different

        # export docx with yaml
        ofile  = os.path.join(self.scratchdir, "omstest_manuscript_yaml.docx")
        print("Running oms for base test with yaml manuscript file")
        os.system("./oms --manuscriptdir {} --manuscriptfile {} --authorfile {} --outputfile {}".format(msdir, msfile_yaml, afile_yaml, ofile))
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
        print("Running oms outline")
        os.system("./oms outline --manuscriptdir {} --manuscriptfile {} --authorfile {} --outputfile {}".format(msdir, msfile, afile, ofile))
        self.assertTrue( filecmp.cmp(ofile, ofile_gold), 'outline files differ')

        # export outline
        basefile = "omstest_manuscript_outline_settings.html"
        ofile = os.path.join(self.scratchdir, basefile) 
        # ofile_gold is the same as the one for the test above
        print("Running oms outline with settings file")
        os.system("./oms outline --settingsfile {}/{} --manuscriptdir {} --manuscriptfile {} --outputfile {}".format(msdir, sfile, msdir, msfile, ofile))
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

        # test query
        print("Running oms query tests ...")
        output = self.cmdline("./oms query --manuscriptfile ../example/manuscript.json --current")
        self.assertEqual( output.decode("utf-8"), "No current chapter found\n")

        output = self.cmdline("./oms query --manuscriptfile ../example/manuscript.yaml --current")
        self.assertEqual( output.decode("utf-8"), "No current chapter found\n")

        output = self.cmdline("./oms query --manuscriptfile ../example/manuscript.yaml --chapters")
        self.assertEqual( output.decode("utf-8"), "Quote\nSynopsis\nSimple Text\nA Chapter Can Be Named Anything That You Can Possibly Imagine in All of The World ... And So Can A Scene\nLists\nLinks\nComments\nNotes\nFootnotes\nEnd\n")

        output = self.cmdline("./oms query --manuscriptfile ../example/manuscript.yaml --chapter \"Simple Text\"")
        self.assertEqual( output.decode("utf-8"), "\nSimple Text\n['003', '002', '001']\n\nAn important scene.\n")

    def cmdline(self, command):
        process = Popen(
            args=command,
            stdout=PIPE,
            shell=True
        )
        return process.communicate()[0]
