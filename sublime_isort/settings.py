# -*- coding: utf-8 -*-
import sublime


def get(view, name, default=None):
    global_settings = sublime.load_settings('isort.sublime-settings')
    project_settings = view.settings().get('isort', {})
    return project_settings.get(name, global_settings.get(name, default))
