import os
import re
import subprocess
import tempfile

import sublime
import sublime_plugin

from . import settings

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


class IsortCommand(sublime_plugin.TextCommand):
    PYTHON_SYNTAX_REGEX = re.compile(r'^Packages\/.+\/Python.*\.tmLanguage$')

    view = None

    def get_region(self, view):
        return sublime.Region(0, view.size())

    def get_buffer_contents(self, view):
        return view.substr(self.get_region(view))

    def set_view(self):
        self.view = sublime.active_window().active_view()
        return self.view

    def get_view(self):
        if self.view is None:
            return self.set_view()

        return self.view

    def set_cursor_back(self, begin_positions):
        this_view = self.get_view()
        for pos in begin_positions:
            this_view.sel().add(pos)

    def get_positions(self):
        pos = []
        for region in self.get_view().sel():
            pos.append(region)
        return pos

    def get_settings(self):
        profile = sublime.active_window().active_view().settings().get('isort')
        return profile or {}

    @property
    def is_python(self):
        current_syntax = self.get_view().settings().get('syntax')
        return bool(self.PYTHON_SYNTAX_REGEX.match(current_syntax))

    def run(self, edit):
        this_view = self.get_view()

        if not self.is_python:
            return

        current_positions = self.get_positions()

        this_contents = self.get_buffer_contents(this_view)
        try:
            sorted_imports = self._execute_isort(
                code=this_contents,
                filename=this_view.file_name()
            )
        except Exception as e:
            sublime.error_message(
                'An error occurred while executing isort: %s' % e
            )
        else:
            this_view.replace(edit, self.get_region(this_view), sorted_imports)

            # Our sel has moved now..
            remove_sel = this_view.sel()[0]
            this_view.sel().subtract(remove_sel)
            self.set_cursor_back(current_positions)

    def _execute_isort(self, code, filename):
        args = [
            settings.get(
                view=self.get_view(),
                name='python_bin',
                default='python'
            ),
            'isort.py',
            '--stdout',
        ]
        if filename:
            settings_path = os.path.dirname(filename)
            args.append('--settings-path')
            args.append(settings_path)

        with tempfile.NamedTemporaryFile() as f:
            f.write(code.encode('utf-8'))
            f.flush()
            output = check_output(args + [f.name], cwd=CURRENT_DIR)

        return output.decode('utf-8')


def check_output(*popenargs, **kwargs):
    process = subprocess.Popen(
        stdout=subprocess.PIPE,
        *popenargs,
        **kwargs
    )
    output, _ = process.communicate()
    return_code = process.poll()
    if return_code:
        cmd = kwargs.get("args")
        if cmd is None:
            cmd = popenargs[0]
        raise subprocess.CalledProcessError(return_code, cmd)
    return output
