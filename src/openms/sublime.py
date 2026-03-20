"""
openms/sublime.py

Implements the `oms sublime` subcommand.

Finds manuscript.yaml (in the given directory or CWD), writes a
.sublime-project file that tells the OpenManuscript Sublime plugin
where to find the data, then opens the project in Sublime Text.
"""

import os
import json
import subprocess
import sys


SUBLIME_EXECUTABLES = [
    "subl",                                         # on PATH (most installs)
    "/Applications/Sublime Text.app/Contents/SharedSupport/bin/subl",  # macOS default
    "C:\\Program Files\\Sublime Text\\subl.exe",   # Windows default
]


def _find_subl():
    """Return the first subl executable we can find, or None."""
    for candidate in SUBLIME_EXECUTABLES:
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return candidate
    # also try which/where
    try:
        result = subprocess.run(
            ["which", "subl"], capture_output=True, text=True
        )
        if result.returncode == 0:
            path = result.stdout.strip()
            if path:
                return path
    except FileNotFoundError:
        pass
    return None


def _find_manuscript_yaml(directory):
    """
    Walk up from `directory` looking for manuscript.yaml.
    Returns absolute path if found, else None.
    """
    current = os.path.abspath(directory)
    while True:
        candidate = os.path.join(current, "manuscript.yaml")
        if os.path.isfile(candidate):
            return candidate
        parent = os.path.dirname(current)
        if parent == current:
            break
        current = parent
    return None


def _write_sublime_project(manuscript_yaml_path):
    """
    Write (or update) a .sublime-project file next to manuscript.yaml.
    Returns the path to the .sublime-project file.
    """
    project_dir = os.path.dirname(manuscript_yaml_path)

    # use the directory name as the project name
    project_name = os.path.basename(project_dir)
    project_file = os.path.join(project_dir, "{}.sublime-project".format(project_name))

    # load existing project data if present
    if os.path.isfile(project_file):
        with open(project_file, "r") as f:
            try:
                project_data = json.load(f)
            except json.JSONDecodeError:
                project_data = {}
    else:
        project_data = {}

    # ensure folders includes the project root
    folders = project_data.get("folders", [])
    folder_paths = [f.get("path") for f in folders]
    if "." not in folder_paths and project_dir not in folder_paths:
        folders.insert(0, {"path": "."})
    project_data["folders"] = folders

    # write the manuscript_yaml path (relative to the project file)
    rel_yaml = os.path.relpath(manuscript_yaml_path, project_dir)
    project_data.setdefault("settings", {})
    project_data["settings"]["manuscript_yaml"] = rel_yaml

    with open(project_file, "w") as f:
        json.dump(project_data, f, indent=4)
        f.write("\n")

    return project_file


def execute(args):
    """Entry point called by the `oms sublime` subcommand."""

    # resolve search directory
    search_dir = getattr(args, "manuscriptdir", None) or os.getcwd()
    search_dir = os.path.abspath(search_dir)

    # find manuscript.yaml
    yaml_path = _find_manuscript_yaml(search_dir)
    if not yaml_path:
        print("ERROR: could not find manuscript.yaml in {} or any parent directory.".format(
            search_dir
        ))
        sys.exit(1)

    print("Found: {}".format(yaml_path))

    # write .sublime-project
    project_file = _write_sublime_project(yaml_path)
    print("Project: {}".format(project_file))

    # find subl
    subl = _find_subl()
    if not subl:
        print(
            "WARNING: could not find the `subl` command.\n"
            "Please open the project manually:\n  {}".format(project_file)
        )
        sys.exit(0)

    # open Sublime
    cmd = [subl, "--project", project_file]
    print("Opening: {}".format(" ".join(cmd)))
    subprocess.Popen(cmd)
