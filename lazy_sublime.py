import sublime
import sublime_plugin
from lazy_unit_tester.create_tests import CreateTests


class LazyCommand(sublime_plugin.TextCommand):
    def run(self, view):
        fileName = self.view.file_name()
        instance = CreateTests(fileName, False, False)
        instance.write_tests()
        sublime.active_window().open_file(instance.unittestFilePath)
