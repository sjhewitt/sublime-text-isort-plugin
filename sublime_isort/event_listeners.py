# -*- coding: utf-8 -*-
import sublime_plugin

from . import settings


class IsortOnSave(sublime_plugin.EventListener):
    @staticmethod
    def is_enabled(view):
        return settings.get(view, 'isort_on_save', default=True)

    def on_pre_save(self, view):
        if self.is_enabled(view):
            view.run_command('isort')
