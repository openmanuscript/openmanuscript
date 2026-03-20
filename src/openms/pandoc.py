"""
openms/pandoc.py

Renders an OpenManuscript project to a Word (docx) file using pandoc
and a pandoc-templates installation.

Pandoc templates are located via (in order of priority):
  1. settings file JSON key "pandoc_templates_dir"
  2. The environment variable OMS_PANDOC_TEMPLATES
  3. The default path ~/bin/pandoc-templates
"""

import os
import json
import sys
import tempfile
import datetime
import yaml

from . import core


# ---------------------------------------------------------------------------
# defaults
# ---------------------------------------------------------------------------

DEFAULT_PANDOC_TEMPLATES = os.path.join(os.environ["HOME"], "bin", "pandoc-templates")


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _load_data_file(path):
    """Load a JSON or YAML data file, return the parsed dict."""
    if not os.path.isfile(path):
        print("ERROR: file not found: {}".format(path))
        sys.exit(1)
    with open(path, "r") as f:
        if path.endswith(".json"):
            return json.load(f)
        elif path.endswith(".yaml") or path.endswith(".yml"):
            return yaml.load(f, Loader=yaml.FullLoader)
        else:
            print("ERROR: unsupported file type: {}".format(path))
            sys.exit(1)


def _include_chapter(chapter):
    return chapter.get("state", "") in ("", "on")


def _find_pandoc_templates():
    """
    Locate the pandoc-templates directory using (in order):
      1. core settings key 'pandoc_templates_dir'
      2. OMS_PANDOC_TEMPLATES environment variable
      3. ~/bin/pandoc-templates
    """
    path = (
        core.get_setting("pandoc_templates_dir")
        or os.environ.get("OMS_PANDOC_TEMPLATES")
        or DEFAULT_PANDOC_TEMPLATES
    )
    return os.path.expanduser(path)


# ---------------------------------------------------------------------------
# metadata file writer
# ---------------------------------------------------------------------------

def _write_metadata_file(author_path, manuscript_path, date, commit, output_path):
    """Write a pandoc-compatible YAML metadata file."""
    adata = _load_data_file(author_path)
    mdata = _load_data_file(manuscript_path)

    a = adata.get("author", adata)
    m = mdata.get("manuscript", mdata)

    with open(output_path, "w") as f:
        f.write("---\n")
        f.write("title: \"{}\"\n".format(m.get("title", "")))
        f.write("short_title: \"{}\"\n".format(m.get("runningtitle", "")))
        f.write("author: \"{}\"\n".format(a.get("name", "")))
        f.write("author_lastname: \"{}\"\n".format(a.get("surname", "")))
        f.write("contact_name: \"{}\"\n".format(a.get("name", "")))
        f.write("contact_address: \"{}\"\n".format(a.get("streetAddress", "")))
        f.write("contact_city_state_zip: \"{}, {} {}\"\n".format(
            a.get("addressLocality", ""),
            a.get("addressRegion", ""),
            a.get("postalCode", "")
        ))
        f.write("contact_phone: \"{}\"\n".format(a.get("phone", "")))
        f.write("contact_email: \"{}\"\n".format(a.get("email", "")))
        f.write("date: \"{}\"\n".format(date))
        f.write("footer_right: \"{}\"\n".format(commit))
        f.write("footer_left: \"{}\"\n".format(manuscript_path))
        f.write("---\n")


# ---------------------------------------------------------------------------
# markdown file writer
# ---------------------------------------------------------------------------

def _write_markdown_file(manuscript_path, scenes_dir, chaptersummary, output_path):
    """Assemble the full manuscript as a single markdown file."""
    mdata = _load_data_file(manuscript_path)
    ms = mdata.get("manuscript", mdata)

    with open(output_path, "w") as f:
        cur = 1
        for chapter in ms.get("chapters", []):
            if not _include_chapter(chapter):
                continue

            f.write("\n")
            f.write("# {}. {}\n".format(cur, chapter.get("title", "")))
            f.write("\n")

            first = True

            if chaptersummary:
                for desc_scene in chapter.get("desc", []):
                    scene_path = os.path.join(scenes_dir, desc_scene + ".md")
                    if os.path.isfile(scene_path):
                        f.write("\n")
                        f.write(open(scene_path).read())
                    else:
                        print("WARNING: desc scene not found: {}".format(scene_path))
            else:
                for scene in chapter.get("scenes", []):
                    scene_path = os.path.join(scenes_dir, scene + ".md")
                    if not os.path.isfile(scene_path):
                        print("WARNING: scene not found: {}".format(scene_path))
                        continue

                    if not first:
                        f.write("\n---\n\n")
                    else:
                        f.write("\n")
                        first = False

                    f.write(open(scene_path).read())

            cur += 1


# ---------------------------------------------------------------------------
# main render function — called directly by default.py
# ---------------------------------------------------------------------------

def render():
    """
    Render the current manuscript to docx using pandoc.
    Reads all options from openms.core.settings.
    """

    author_file     = core.get_authorfile()
    manuscript_file = core.get_manuscriptfile()
    output_file     = core.get_setting("outputfile")
    font            = core.get_setting("font") or "Courier"
    toc             = core.get_setting("toc") or False
    chaptersummary  = core.get_setting("chaptersummary") or False
    commit          = core.get_setting("commit") or ""
    verbose         = core.get_setting("verbose") or False

    # handle date
    date_setting = core.get_setting("date")
    if date_setting == "now":
        date = "{dt:%b} {dt.day}, {dt.year} {dt:%l}:{dt:%M}{dt:%p}".format(
            dt=datetime.datetime.now()
        )
    elif date_setting:
        date = date_setting
    else:
        date = ""

    # locate pandoc templates
    pandoc_dir  = _find_pandoc_templates()
    pandoc_exec = os.path.join(pandoc_dir, "bin", "md2long.sh")

    if not os.path.isdir(pandoc_dir):
        print("ERROR: pandoc-templates directory not found: {}".format(pandoc_dir))
        print("Set 'pandoc_templates_dir' in your settings file, or set the")
        print("OMS_PANDOC_TEMPLATES environment variable.")
        sys.exit(1)

    if not os.path.isfile(pandoc_exec):
        print("ERROR: pandoc script not found: {}".format(pandoc_exec))
        sys.exit(1)

    # scenes directory sits next to manuscript file
    scenes_dir = os.path.join(
        os.path.dirname(os.path.abspath(manuscript_file)), "scenes"
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_md       = os.path.join(tmpdir, "manuscript.md")
        tmp_metadata = os.path.join(tmpdir, "metadata.md")

        _write_markdown_file(manuscript_file, scenes_dir, chaptersummary, tmp_md)
        _write_metadata_file(author_file, manuscript_file, date, commit, tmp_metadata)

        toc_flag        = "--toc" if toc else ""
        modern_flag     = "--modern" if font.lower() == "times" else ""
        verbose_redirect = "" if verbose else " > /dev/null"

        command = "{} {} {} --output {} --overwrite --from=markdown {} {} {}".format(
            pandoc_exec,
            toc_flag,
            modern_flag,
            output_file,
            tmp_metadata,
            tmp_md,
            verbose_redirect
        )

        if verbose:
            print("Running: {}".format(command))

        os.system(command)

    if os.path.isfile(output_file):
        print("Written: {}".format(output_file))
    else:
        print("ERROR: output file was not created: {}".format(output_file))
        sys.exit(1)
