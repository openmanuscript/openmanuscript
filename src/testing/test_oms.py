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

    # clean up
    def tearDown(self):
        clean = True
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
        bfile = "omstest_manuscript.docx"
        ofile = os.path.join(self.scratchdir, bfile) 
        gfile = os.path.join(self.golddir, bfile) 
        print("Running oms for base test")
        os.system("./oms --manuscriptdir {} --manuscriptfile {} --authorfile {} --outputfile {}".format(msdir, msfile, afile, ofile))
        self.compare_docx_files( ofile, gfile )

        # export docx
        bfile = "omstest_manuscript_toc.docx"
        ofile = os.path.join(self.scratchdir, bfile) 
        gfile = os.path.join(self.golddir, bfile) 
        print("Running oms for base test with toc")
        os.system("./oms --manuscriptdir {} --manuscriptfile {} --authorfile {} --outputfile {} --toc".format(msdir, msfile, afile, ofile))
        self.compare_docx_files( ofile, gfile )

        # export docx with yaml
        bfile = "omstest_manuscript_yaml.docx"
        ofile = os.path.join(self.scratchdir, bfile) 
        gfile = os.path.join(self.golddir, bfile) 
        print("Running oms for base test with yaml manuscript file")
        os.system("./oms --manuscriptdir {} --manuscriptfile {} --authorfile {} --outputfile {}".format(msdir, msfile_yaml, afile_yaml, ofile))
        self.compare_docx_files( ofile, gfile )

        # export docx with settings file, additional command line argument and 
        # command line argument override
        bfile = "omstest_settings.docx"
        ofile = os.path.join(self.scratchdir, bfile) 
        gfile = os.path.join(self.golddir, bfile) 
        print("Running oms for settings file test")
        os.system("./oms --settingsfile {}/{} --manuscriptdir {} --outputfile {}".format(msdir, sfile, msdir, ofile))
        self.compare_docx_files( ofile, gfile )

        # export docx
        bfile = "omstest_manuscript_noquote-nosynopsis.docx"
        ofile = os.path.join(self.scratchdir, bfile) 
        gfile = os.path.join(self.golddir, bfile) 
        print("Running oms for no quote no synopsis")
        os.system("./oms --excludetags quote synopsis --manuscriptdir {} --manuscriptfile {} --authorfile {} --outputfile {}".format(msdir, msfile, afile, ofile))
        self.compare_docx_files( ofile, gfile )
        
        # export docx
        bfile = "omstest_manuscript_simple.docx"
        ofile = os.path.join(self.scratchdir, bfile) 
        gfile = os.path.join(self.golddir, bfile) 
        print("Running oms for simple test")
        os.system("./oms --includetags simple --excludetags quote synopsis --manuscriptdir {} --manuscriptfile {} --authorfile {} --outputfile {}".format(msdir, msfile, afile, ofile))
        self.compare_docx_files( ofile, gfile )
        
        # export docx
        bfile = "omstest_manuscript_notes.docx"
        ofile = os.path.join(self.scratchdir, bfile) 
        gfile = os.path.join(self.golddir, bfile) 
        print("Running oms for notes")
        os.system("./oms --notes --manuscriptdir {} --manuscriptfile {} --authorfile {} --outputfile {}".format(msdir, msfile, afile, ofile))
        self.compare_docx_files( ofile, gfile )

        # export docx
            # don't exclude
        bfile = "omstest_manuscript_dont-exclude.docx"
        ofile = os.path.join(self.scratchdir, bfile) 
        gfile = os.path.join(self.golddir, bfile) 
        emsfile = "exclude.json"
        print("Running oms for exclude check (don't exclude)")
        os.system("./oms --notes --manuscriptdir {} --manuscriptfile {} \
                        --authorfile {} --outputfile {} --excludesections {} --includesections {}".format(
                         msdir, emsfile, afile, ofile, extest[1], extest[0]))
        self.compare_docx_files( ofile, gfile )
            # exclude
        bfile = "omstest_manuscript_exclude.docx"
        ofile = os.path.join(self.scratchdir, bfile) 
        gfile = os.path.join(self.golddir, bfile) 
        print("Running oms for exclude check (exclude)")
        os.system("./oms --notes --manuscriptdir {} --manuscriptfile {} \
                        --authorfile {} --outputfile {} --excludesections {} --includesections {}".format(
                         msdir, emsfile, afile, ofile, extest[0], extest[1]))
        self.compare_docx_files( ofile, gfile )

        # export outline
        bfile = "omstest_manuscript_outline.html"
        ofile = os.path.join(self.scratchdir, bfile) 
        gfile = os.path.join(self.golddir, bfile) 
        print("Running oms outline")
        os.system("./oms outline --manuscriptdir {} --manuscriptfile {} --authorfile {} --outputfile {}".format(msdir, msfile, afile, ofile))
        self.assertTrue( filecmp.cmp(ofile, gfile), 'outline files differ')

        # export outline
        bfile = "omstest_manuscript_outline_settings.html"
        ofile = os.path.join(self.scratchdir, bfile) 
        gfile = os.path.join(self.golddir, bfile) 
        sfile = "outline.json"
        # gfile is the same as the one for the test above
        print("Running oms outline with settings file")
        os.system("./oms outline --settingsfile {}/{} --manuscriptdir {}".format(msdir, sfile, msdir))
        self.assertTrue( filecmp.cmp(ofile, gfile), 'outline files differ')

        # test template 
        testdir = os.path.join(self.scratchdir, "template")
        os.mkdir(testdir)
        openms.template.write_template(testdir)

        # test short story 
        bfile = "omstest_manuscript_shortstory.docx"
        ofile = os.path.join(self.scratchdir, bfile) 
        gfile = os.path.join(self.golddir, bfile) 
        print("Running oms for short story")
        msfile = "short.json"
        os.system("./oms --manuscripttype story --notes --manuscriptdir {} --manuscriptfile {} --authorfile {} --outputfile {}".format(msdir, msfile, afile, ofile))
        self.compare_docx_files( ofile, gfile )

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

    #
    # compare docx files, but first remove the creation date, which causes them
    # to be different
    #
    def compare_docx_files( self, one, two ):
        cdir = os.path.join( self.scratchdir, "docx_diff_test" )
        os.mkdir( cdir )

        # unzip the docx files for comparison
        onezip = os.path.join(cdir, "01.zip")
        twozip = os.path.join(cdir, "02.zip")
        os.system("unzip {} -d {} 2>&1 > /dev/null".format( one, onezip ))
        # remove the creation date
        os.system("sed -i \'\' \'s/<dcterms:created.*created>//g\' {}/docProps/core.xml".format(onezip))
        os.system("unzip {} -d {} 2>&1 > /dev/null".format( two, twozip ))
        # remove the creation date
        os.system("sed -i \'\' \'s/<dcterms:created.*created>//g\' {}/docProps/core.xml".format(twozip))

        # print("compare: {} {}".format(onezip, twozip))
        output = self.cmdline("diff -r {} {}".format( onezip, twozip ))
        self.assertEqual( output.decode("utf-8"), "", "docx files differ")

        # remove the unzipped files
        os.system("rm -rf {}".format( cdir ))
