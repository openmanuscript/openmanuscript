import unittest
import os
import filecmp
import shutil
import openms
import sys
from subprocess import PIPE, Popen

class TestCIS(unittest.TestCase):

    # setting for better output for CIS
    maxDiff = None

    def setUp(self):
        self.scratchdir = os.path.join("testing", "scratch") 
        self.golddir    = os.path.join("testing", "gold")

    # clean up
    def tearDown(self):
        clean = False
        if clean:
            shutil.rmtree( self.scratchdir )
        else:
            print("Not cleaning up from test ...")

    def test_oms(self):
        # settings for tests
        msdir  = "../example"
        msfile = "manuscript.json"
        msfile_exclude = "exclude.json"
        msfile_minimal = "manuscript_minimal_data.yaml"
        msfile_short = "short.json"
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

        # export with slug
        bfile = "omstest_manuscript_slug.docx"
        ofile = os.path.join(self.scratchdir, bfile) 
        gfile = os.path.join(self.golddir, bfile) 
        print("Running oms for base test with slug")
        os.system("./oms --manuscriptdir {} --manuscriptfile {} --authorfile {} \
                        --outputfile {} --slug \"test: this is the slug\"".format(msdir, msfile, afile, ofile))
        self.compare_docx_files( ofile, gfile )

        # export with slug
        bfile = "omstest_minimal_data.docx"
        ofile = os.path.join(self.scratchdir, bfile) 
        gfile = os.path.join(self.golddir, bfile) 
        print("Running oms for base test with minimal data")
        os.system("./oms --manuscriptdir {} --manuscriptfile {} --outputfile {}".format(msdir, msfile_minimal, ofile))
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

        if True:        
            # this test runs locally, but does not pass in Travis CI
            # the problem appears to be the w:t object, which in Travis,
            # includes the 'preserve' attribute:
            #     <w:r><w:t xml:space="preserve">NOTE: The html tag can be anything you want it to be. </w:t></w:r>
            # unable to fix this, so this test can be ignored (redundant with
            # the next test, which reverses the order of the exclude/include)
            # export docx
                # don't exclude
            bfile = "omstest_manuscript_dont-exclude.docx"
            ofile = os.path.join(self.scratchdir, bfile) 
            gfile = os.path.join(self.golddir, bfile) 
            print("Running oms for exclude check (don't exclude)")
            os.system("./oms --notes --manuscriptdir {} --manuscriptfile {} \
                            --authorfile {} --outputfile {} --excludesections {} --includesections {}".format(
                             msdir, msfile_exclude, afile, ofile, extest[1], extest[0]))
            self.compare_docx_files( ofile, gfile )
    
        # this test works both locally and on travis CI
            # excludesection/includesection test
        bfile = "omstest_manuscript_exclude.docx"
        ofile = os.path.join(self.scratchdir, bfile) 
        gfile = os.path.join(self.golddir, bfile) 
        print("Running oms for excludesection/includesection")
        os.system("./oms --notes --manuscriptdir {} --manuscriptfile {} \
                        --authorfile {} --outputfile {} --excludesections {} --includesections {}".format(
                         msdir, msfile_exclude, afile, ofile, extest[0], extest[1]))
        self.compare_docx_files( ofile, gfile )

        # test short story 
        bfile = "omstest_manuscript_shortstory.docx"
        ofile = os.path.join(self.scratchdir, bfile) 
        gfile = os.path.join(self.golddir, bfile) 
        print("Running oms for short story")
        os.system("./oms --manuscripttype story --notes --manuscriptdir {} --manuscriptfile {} --authorfile {} --outputfile {}".format(msdir, msfile_short, afile, ofile))
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


        # test query
        chapter_string = '''Quote
  ['quotes']
Synopsis
  ['synopsis']
Simple Text
  ['003', '002', '001']
A Chapter Can Be Named Anything That You Can Possibly Imagine in All of The World ... And So Can A Scene
  ['This_name', 'look01', 'chapter_i_hate']
Lists
  ['lists']
Links
  ['links']
Comments
  ['comments']
Notes
  ['notes']
Footnotes
  ['footnotes']
End
  ['end']
'''
        print("Running oms query tests")
            # state current, json
        output = self.cmdline("./oms query --manuscriptfile ../example/manuscript.json --state current")
        self.assertEqual( output.decode("utf-8"), "No chapter with state current found\n")
            # state current, yaml
        output = self.cmdline("./oms query --manuscriptfile ../example/manuscript.yaml --state current")
        self.assertEqual( output.decode("utf-8"), "No chapter with state current found\n")
            # tag nothing, json
        output = self.cmdline("./oms query --manuscriptfile ../example/manuscript.json --tag nothing")
        self.assertEqual( output.decode("utf-8"), "No chapter with tag nothing found\n")
            # tag nothing, yaml
        output = self.cmdline("./oms query --manuscriptfile ../example/manuscript.yaml --tag nothing")
        self.assertEqual( output.decode("utf-8"), "No chapter with tag nothing found\n")
            # chapters
        output = self.cmdline("./oms query --manuscriptfile ../example/manuscript.yaml --chapters")
        self.assertEqual( output.decode("utf-8"), chapter_string ) 
            # single chapter
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
        # print("compare: {} {}".format(one, two))
        cdir = os.path.join( self.scratchdir, "docx_diff_test" )
        os.mkdir( cdir )

        # unzip the docx files for comparison
        onezip = os.path.join(cdir, "01.zip")
        twozip = os.path.join(cdir, "02.zip")

        # remove known data that can cause a difference
        os.system("unzip {} -d {} 2>&1 > /dev/null".format( one, onezip ))
        self.strip_known_conflics( onezip )

        os.system("unzip {} -d {} 2>&1 > /dev/null".format( two, twozip ))
        self.strip_known_conflics( twozip )

        # print("compare: {} {}".format(onezip, twozip))
        output = self.cmdline("diff -r {} {}".format( onezip, twozip ))
        self.assertEqual( output.decode("utf-8"), "", "docx files differ")

        # remove the unzipped files
        os.system("rm -rf {}".format( cdir ))

    def strip_known_conflics( self, zipdir ):
        # determine platform, and use the appropriate syntax for sed
        if sys.platform == "darwin":
            # remove the creation date
            os.system("sed -i \'\' \'s/<dcterms:created.*created>//g\' {}/docProps/core.xml".format(zipdir))
            # remove the version string 
            os.system("sed -i \'\' \'s/<dc:description>.*dc:description>//g\' {}/docProps/core.xml".format(zipdir))
        else:
            # remove the creation date
            os.system("sed -i \'s/<dcterms:created.*created>//g\' {}/docProps/core.xml".format(zipdir))
            # remove the version string 
            os.system("sed -i \'s/<dc:description>.*dc:description>//g\' {}/docProps/core.xml".format(zipdir))
