"""
OpenManuscript - Sublime Text 4 Plugin
Provides quick-panel navigation of OpenManuscript projects.

Install: copy the OpenManuscript/ folder to:
  ~/Library/Application Support/Sublime Text/Packages/   (macOS)
  ~/.config/sublime-text/Packages/                       (Linux)
  %APPDATA%\Sublime Text\Packages\                       (Windows)
"""

import sublime
import sublime_plugin
import os
import sys
import os
sys.path.append(os.path.dirname(__file__))
import sublime
import sublime_plugin
import yaml


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _find_manuscript_yaml(window):
    """
    Find manuscript.yaml by checking in order:
      1. project settings key 'manuscript_yaml' (absolute or relative to project)
      2. first folder in the project root
      3. directory of the currently active file
    Returns absolute path string or None.
    """
    project_data = window.project_data() or {}
    settings = project_data.get("settings", {})
    ms_path = settings.get("manuscript_yaml")
    if ms_path:
        if not os.path.isabs(ms_path):
            project_file = window.project_file_name()
            if project_file:
                base = os.path.dirname(project_file)
                ms_path = os.path.join(base, ms_path)
        if os.path.isfile(ms_path):
            return ms_path

    folders = window.folders()
    if folders:
        candidate = os.path.join(folders[0], "manuscript.yaml")
        if os.path.isfile(candidate):
            return candidate

    view = window.active_view()
    if view and view.file_name():
        candidate = os.path.join(os.path.dirname(view.file_name()), "manuscript.yaml")
        if os.path.isfile(candidate):
            return candidate

    return None


def _load_manuscript(yaml_path):
    """Load and return the manuscript dict, or None on error."""
    try:
        with open(yaml_path, "r") as f:
            data = yaml.safe_load(f)
        return data.get("manuscript", {})
    except Exception as e:
        sublime.error_message("OpenManuscript: could not read {}\n{}".format(yaml_path, e))
        return None


def _scenes_dir(yaml_path):
    return os.path.join(os.path.dirname(yaml_path), "scenes")


def _scene_filepath(scenes_dir, scene_name):
    if scene_name.endswith(".md"):
        return os.path.join(scenes_dir, scene_name)
    return os.path.join(scenes_dir, scene_name + ".md")


# ---------------------------------------------------------------------------
# command: flat list navigator
# ---------------------------------------------------------------------------

class OpenManuscriptNavigatorCommand(sublime_plugin.WindowCommand):
    """
    Show a single flat quick panel:

      Chapter 1: The Beginning       3 scenes
          001
          002
          003
      Chapter 2: The Middle          2 scenes
          004
          005

    Selecting a chapter header opens its first scene.
    Selecting a scene opens that scene file.

    Keybinding:
      { "keys": ["ctrl+shift+m"], "command": "open_manuscript_navigator" }
    """

    def run(self):
        yaml_path = _find_manuscript_yaml(self.window)
        if not yaml_path:
            sublime.error_message(
                "OpenManuscript: no manuscript.yaml found.\n\n"
                "Run  oms sublime  in your project directory, or add\n"
                "  \"settings\": {\"manuscript_yaml\": \"<path>\"}\n"
                "to your .sublime-project file."
            )
            return

        manuscript = _load_manuscript(yaml_path)
        if manuscript is None:
            return

        chapters = manuscript.get("chapters", [])
        if not chapters:
            sublime.message_dialog("OpenManuscript: no chapters found in manuscript.yaml")
            return

        scenes_dir = _scenes_dir(yaml_path)
        items = []
        self._actions = []

        chapter_num = 0
        for ch in chapters:
            ch_type = ch.get("type", "chapter").lower()
            is_numbered = ch_type not in ("quote", "synopsis")
            if is_numbered:
                chapter_num += 1

            title = ch.get("title", "(untitled)")
            chapter_label = "Chapter {}: {}".format(chapter_num, title) if is_numbered else title

            scenes = ch.get("scenes", [])

            # find first valid scene file for this chapter
            first_scene_path = None
            for s in scenes:
                p = _scene_filepath(scenes_dir, s)
                if os.path.isfile(p):
                    first_scene_path = p
                    break

            # chapter header row
            items.append(sublime.QuickPanelItem(
                trigger=chapter_label,
                details="",
                annotation="{} scene{}".format(len(scenes), "s" if len(scenes) != 1 else ""),
                kind=sublime.KIND_FUNCTION
            ))
            self._actions.append({"type": "chapter", "first_scene": first_scene_path})

            # scene rows — indented with non-breaking spaces
            for scene_name in scenes:
                scene_path = _scene_filepath(scenes_dir, scene_name)
                exists = os.path.isfile(scene_path)

                items.append(sublime.QuickPanelItem(
                    trigger="\u00a0\u00a0\u00a0\u00a0{}".format(scene_name),
                    details="",
                    annotation="" if exists else "missing",
                    kind=sublime.KIND_SNIPPET if exists else sublime.KIND_AMBIGUOUS
                ))
                self._actions.append({"type": "scene", "path": scene_path, "exists": exists})

        self.window.show_quick_panel(
            items,
            self._on_select,
            placeholder="Navigate manuscript\u2026"
        )

    def _on_select(self, index):
        if index < 0:
            return

        action = self._actions[index]

        if action["type"] == "chapter":
            path = action.get("first_scene")
            if path:
                self.window.open_file(path)
            else:
                sublime.message_dialog("No scene files found for this chapter.")

        elif action["type"] == "scene":
            path = action["path"]
            if action.get("exists"):
                self.window.open_file(path)
            else:
                if sublime.ok_cancel_dialog(
                    "Scene file not found:\n{}\n\nCreate it?".format(path),
                    "Create"
                ):
                    _create_scene_file(path)
                    self.window.open_file(path)


# ---------------------------------------------------------------------------
# command: jump to manuscript.yaml
# ---------------------------------------------------------------------------

class OpenManuscriptYamlCommand(sublime_plugin.WindowCommand):
    """
    Open manuscript.yaml in the editor.
    Keybinding:
      { "keys": ["ctrl+shift+y"], "command": "open_manuscript_yaml" }
    """

    def run(self):
        yaml_path = _find_manuscript_yaml(self.window)
        if not yaml_path:
            sublime.error_message("OpenManuscript: no manuscript.yaml found.")
            return
        self.window.open_file(yaml_path)


# ---------------------------------------------------------------------------
# command: word count stats
# ---------------------------------------------------------------------------

class OpenManuscriptStatsCommand(sublime_plugin.WindowCommand):
    """
    Show word counts per chapter in the Sublime output panel.
    Keybinding:
      { "keys": ["ctrl+shift+w"], "command": "open_manuscript_stats" }
    """

    def run(self):
        yaml_path = _find_manuscript_yaml(self.window)
        if not yaml_path:
            sublime.error_message("OpenManuscript: no manuscript.yaml found.")
            return

        manuscript = _load_manuscript(yaml_path)
        if manuscript is None:
            return

        scenes_dir = _scenes_dir(yaml_path)
        chapters = manuscript.get("chapters", [])
        title = manuscript.get("title", "Untitled")

        lines = []
        lines.append("OpenManuscript \u2014 {}".format(title))
        lines.append("=" * 60)

        total = 0
        chapter_num = 0
        for ch in chapters:
            ch_type = ch.get("type", "chapter").lower()
            is_numbered = ch_type not in ("quote", "synopsis")
            if is_numbered:
                chapter_num += 1

            ch_title = ch.get("title", "(untitled)")
            scenes = ch.get("scenes", [])
            ch_words = 0
            for scene_name in scenes:
                scene_file = _scene_filepath(scenes_dir, scene_name)
                if os.path.isfile(scene_file):
                    ch_words += _word_count(scene_file)
            total += ch_words

            label = "Chapter {}: {}".format(chapter_num, ch_title) if is_numbered else ch_title
            lines.append("  {:<48} {:>6,} words".format(label[:48], ch_words))

        lines.append("-" * 60)
        lines.append("  {:<48} {:>6,} words total".format("", total))
        lines.append("")

        panel = self.window.create_output_panel("openmanuscript")
        panel.set_read_only(False)
        panel.run_command("append", {"characters": "\n".join(lines)})
        panel.set_read_only(True)
        self.window.run_command("show_panel", {"panel": "output.openmanuscript"})


# ---------------------------------------------------------------------------
# utilities
# ---------------------------------------------------------------------------

def _word_count(filepath):
    count = 0
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            count += len(line.split())
    return count


def _create_scene_file(filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    scene_name = os.path.splitext(os.path.basename(filepath))[0]
    with open(filepath, "w") as f:
        f.write("<!-- scene: {} -->\n\n".format(scene_name))
