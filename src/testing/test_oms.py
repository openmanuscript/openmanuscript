import unittest
import os
import filecmp
import shutil
import json
import yaml
import sys
import tempfile
from subprocess import PIPE, Popen
from unittest.mock import patch

import openms
import openms.pandoc


class TestOms(unittest.TestCase):

    maxDiff = None

    def setUp(self):
        self.scratchdir = os.path.join("testing", "scratch")
        self.golddir    = os.path.join("testing", "gold")
        self.exampledir = "../example"
        self.msfile     = "manuscript.json"
        self.msfile_yaml = "manuscript.yaml"
        self.msfile_minimal = "manuscript_minimal_data.yaml"
        self.msfile_short = "short.json"
        self.afile      = "author.json"
        self.afile_yaml = "author.yaml"
        os.makedirs(self.scratchdir, exist_ok=True)

    def tearDown(self):
        clean = False
        if clean:
            shutil.rmtree(self.scratchdir)

    # -----------------------------------------------------------------------
    # helpers
    # -----------------------------------------------------------------------

    def cmdline(self, command):
        process = Popen(args=command, stdout=PIPE, shell=True)
        return process.communicate()[0]

    def pandoc_available(self):
        """Return True if pandoc is installed and templates are accessible."""
        result = self.cmdline("which pandoc")
        if not result.strip():
            return False
        templates_dir = os.path.expanduser(
            os.environ.get("OMS_PANDOC_TEMPLATES", "~/bin/pandoc-templates")
        )
        return os.path.isdir(templates_dir)

    # -----------------------------------------------------------------------
    # query tests — unaffected by rendering refactor
    # -----------------------------------------------------------------------

    def test_query_state(self):
        """Query: no chapter with state 'current' (json)."""
        output = self.cmdline(
            "./oms query --manuscriptfile ../example/manuscript.json --state current"
        )
        self.assertEqual(output.decode("utf-8"), "No chapter with state current found\n")

    def test_query_state_yaml(self):
        """Query: no chapter with state 'current' (yaml)."""
        output = self.cmdline(
            "./oms query --manuscriptfile ../example/manuscript.yaml --state current"
        )
        self.assertEqual(output.decode("utf-8"), "No chapter with state current found\n")

    def test_query_tag_missing(self):
        """Query: no chapter with tag 'nothing' (json)."""
        output = self.cmdline(
            "./oms query --manuscriptfile ../example/manuscript.json --tag nothing"
        )
        self.assertEqual(output.decode("utf-8"), "No chapter with tag nothing found\n")

    def test_query_tag_missing_yaml(self):
        """Query: no chapter with tag 'nothing' (yaml)."""
        output = self.cmdline(
            "./oms query --manuscriptfile ../example/manuscript.yaml --tag nothing"
        )
        self.assertEqual(output.decode("utf-8"), "No chapter with tag nothing found\n")

    def test_query_chapters(self):
        """Query: list all chapters."""
        expected = (
            "Quote\n"
            "  ['quotes']\n"
            "Synopsis\n"
            "  ['synopsis']\n"
            "Simple Text\n"
            "  ['003', '002', '001']\n"
            "A Chapter Can Be Named Anything That You Can Possibly Imagine in All of The World ... And So Can A Scene\n"
            "  ['This_name', 'look01', 'chapter_i_hate']\n"
            "Lists\n"
            "  ['lists']\n"
            "Links\n"
            "  ['links']\n"
            "Comments\n"
            "  ['comments']\n"
            "Notes\n"
            "  ['notes']\n"
            "Footnotes\n"
            "  ['footnotes']\n"
            "End\n"
            "  ['end']\n"
        )
        output = self.cmdline(
            "./oms query --manuscriptfile ../example/manuscript.yaml --chapters"
        )
        self.assertEqual(output.decode("utf-8"), expected)

    def test_query_single_chapter(self):
        """Query: single chapter detail."""
        output = self.cmdline(
            "./oms query --manuscriptfile ../example/manuscript.yaml --chapter \"Simple Text\""
        )
        self.assertEqual(
            output.decode("utf-8"),
            "\nSimple Text\n['003', '002', '001']\n\nAn important scene.\n"
        )

    # -----------------------------------------------------------------------
    # outline tests — unaffected by rendering refactor
    # -----------------------------------------------------------------------

    def test_outline(self):
        """Outline: HTML output matches gold file."""
        bfile = "omstest_manuscript_outline.html"
        ofile = os.path.join(self.scratchdir, bfile)
        gfile = os.path.join(self.golddir, bfile)
        os.system("./oms outline --manuscriptdir {} --manuscriptfile {} --authorfile {} --outputfile {}".format(
            self.exampledir, self.msfile, self.afile, ofile
        ))
        self.assertTrue(filecmp.cmp(ofile, gfile), "outline files differ")

    def test_outline_settings(self):
        """Outline: HTML output via settings file matches gold file."""
        bfile = "omstest_manuscript_outline_settings.html"
        ofile = os.path.join(self.scratchdir, bfile)
        gfile = os.path.join(self.golddir, bfile)
        os.system("./oms outline --settingsfile {}/{} --manuscriptdir {}".format(
            self.exampledir, "outline.json", self.exampledir
        ))
        self.assertTrue(filecmp.cmp(ofile, gfile), "outline settings files differ")

    # -----------------------------------------------------------------------
    # template test — unaffected by rendering refactor
    # -----------------------------------------------------------------------

    def test_template(self):
        """Template: write_template creates expected files."""
        testdir = os.path.join(self.scratchdir, "template")
        os.makedirs(testdir, exist_ok=True)
        openms.template.write_template(testdir)
        self.assertTrue(os.path.isdir(testdir))

    # -----------------------------------------------------------------------
    # pandoc unit tests — test markdown/metadata assembly without pandoc
    # -----------------------------------------------------------------------

    def test_write_markdown_file_basic(self):
        """Pandoc: markdown file contains chapter titles and scene content."""
        ms_path    = os.path.join(self.exampledir, "m.json")
        scenes_dir = os.path.join(self.exampledir, "scenes")

        with tempfile.NamedTemporaryFile(mode="r", suffix=".md", delete=False) as tmp:
            tmppath = tmp.name

        try:
            openms.pandoc._write_markdown_file(ms_path, scenes_dir, False, tmppath)
            with open(tmppath) as f:
                content = f.read()

            self.assertIn("# 1. Simple Text", content)
            self.assertIn("# 2. A Chapter Can Be Named", content)
            self.assertIn("# 3. Quotes", content)
            # scene separator between scenes in same chapter
            self.assertIn("---", content)
        finally:
            os.unlink(tmppath)

    def test_write_markdown_file_chapter_order(self):
        """Pandoc: chapters appear in manuscript order."""
        ms_path    = os.path.join(self.exampledir, "m.json")
        scenes_dir = os.path.join(self.exampledir, "scenes")

        with tempfile.NamedTemporaryFile(mode="r", suffix=".md", delete=False) as tmp:
            tmppath = tmp.name

        try:
            openms.pandoc._write_markdown_file(ms_path, scenes_dir, False, tmppath)
            with open(tmppath) as f:
                content = f.read()

            pos1 = content.find("# 1. Simple Text")
            pos2 = content.find("# 2. A Chapter Can Be Named")
            pos3 = content.find("# 3. Quotes")
            self.assertLess(pos1, pos2)
            self.assertLess(pos2, pos3)
        finally:
            os.unlink(tmppath)

    def test_write_markdown_excludes_off_chapters(self):
        """Pandoc: chapters with state != 'on'/'' are excluded."""
        ms_data = {
            "version": "2.1",
            "manuscript": {
                "title": "Test",
                "runningtitle": "test",
                "chapters": [
                    {"title": "Included", "scenes": [], "state": "on"},
                    {"title": "Excluded", "scenes": [], "state": "off"},
                ]
            }
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            ms_path = os.path.join(tmpdir, "manuscript.json")
            out_path = os.path.join(tmpdir, "out.md")
            with open(ms_path, "w") as f:
                json.dump(ms_data, f)

            openms.pandoc._write_markdown_file(ms_path, tmpdir, False, out_path)
            with open(out_path) as f:
                content = f.read()

            self.assertIn("Included", content)
            self.assertNotIn("Excluded", content)

    def test_write_metadata_file(self):
        """Pandoc: metadata file contains expected YAML keys."""
        author_path = os.path.join(self.exampledir, self.afile)
        ms_path     = os.path.join(self.exampledir, self.msfile)

        with tempfile.NamedTemporaryFile(mode="r", suffix=".md", delete=False) as tmp:
            tmppath = tmp.name

        try:
            openms.pandoc._write_metadata_file(
                author_path, ms_path, "Jan 1, 2025", "abc123", tmppath
            )
            with open(tmppath) as f:
                content = f.read()

            self.assertIn("title:", content)
            self.assertIn("author:", content)
            self.assertIn("contact_email:", content)
            self.assertIn("Jan 1, 2025", content)
            self.assertIn("abc123", content)
            self.assertTrue(content.startswith("---"))
            self.assertTrue(content.strip().endswith("---"))
        finally:
            os.unlink(tmppath)

    def test_write_metadata_yaml_author(self):
        """Pandoc: metadata file works with yaml author file."""
        author_path = os.path.join(self.exampledir, self.afile_yaml)
        ms_path     = os.path.join(self.exampledir, self.msfile_yaml)

        with tempfile.NamedTemporaryFile(mode="r", suffix=".md", delete=False) as tmp:
            tmppath = tmp.name

        try:
            openms.pandoc._write_metadata_file(
                author_path, ms_path, "", "", tmppath
            )
            with open(tmppath) as f:
                content = f.read()
            self.assertIn("title:", content)
        finally:
            os.unlink(tmppath)

    def test_include_chapter(self):
        """Pandoc: _include_chapter respects state field."""
        self.assertTrue(openms.pandoc._include_chapter({"title": "A"}))
        self.assertTrue(openms.pandoc._include_chapter({"title": "A", "state": "on"}))
        self.assertTrue(openms.pandoc._include_chapter({"title": "A", "state": ""}))
        self.assertFalse(openms.pandoc._include_chapter({"title": "A", "state": "off"}))

    def test_find_pandoc_templates_env(self):
        """Pandoc: OMS_PANDOC_TEMPLATES env var is respected."""
        with patch.dict(os.environ, {"OMS_PANDOC_TEMPLATES": "/custom/path"}):
            # temporarily clear the core setting
            openms.core.set("pandoc_templates_dir", None)
            result = openms.pandoc._find_pandoc_templates()
            self.assertEqual(result, "/custom/path")

    def test_find_pandoc_templates_core_setting(self):
        """Pandoc: core settings key takes priority over env var."""
        openms.core.set("pandoc_templates_dir", "/from/settings")
        with patch.dict(os.environ, {"OMS_PANDOC_TEMPLATES": "/from/env"}):
            result = openms.pandoc._find_pandoc_templates()
            self.assertEqual(result, "/from/settings")
        openms.core.set("pandoc_templates_dir", None)

    # -----------------------------------------------------------------------
    # pandoc integration test — only runs if pandoc + templates are present
    # -----------------------------------------------------------------------

    @unittest.skipUnless(
        os.path.isdir(os.path.expanduser(
            os.environ.get("OMS_PANDOC_TEMPLATES", "~/bin/pandoc-templates")
        )),
        "pandoc templates not available — skipping integration test"
    )
    def test_pandoc_render_integration(self):
        """Pandoc integration: oms produces a non-empty docx file."""
        ofile = os.path.join(self.scratchdir, "omstest_pandoc_integration.docx")

        openms.core.set("authorfile",     self.afile)
        openms.core.set("manuscriptfile", self.msfile)
        openms.core.set("manuscriptdir",  self.exampledir)
        openms.core.set("outputfile",     ofile)
        openms.core.set("font",           "Courier")
        openms.core.set("toc",            False)
        openms.core.set("chaptersummary", False)
        openms.core.set("commit",         "")
        openms.core.set("date",           None)
        openms.core.set("verbose",        False)
        openms.core.read_data()

        openms.pandoc.render()

        self.assertTrue(os.path.isfile(ofile), "docx output file not created")
        self.assertGreater(os.path.getsize(ofile), 1024, "docx output file is too small")


if __name__ == "__main__":
    unittest.main()
