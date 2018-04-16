import sublime
import sublime_plugin
from .create_tests import CreateTests


def create_tests_wrapper(fileName, includeCommented, includeIndented):
    instance = CreateTests(fileName, includeCommented, includeIndented)
    instance.write_tests()
    return instance


class CreatePythonUnittestsCommand(sublime_plugin.TextCommand):
    def run(self, view):
        fileName = self.view.file_name()
        instance = create_tests_wrapper(fileName, False, False)
        sublime.active_window().open_file(instance.unittestFilePath)


class CreatePythonUnittestsIncludeCommentedCommand(sublime_plugin.TextCommand):
    def run(self, view):
        fileName = self.view.file_name()
        instance = create_tests_wrapper(fileName, True, False)
        sublime.active_window().open_file(instance.unittestFilePath)


class CreatePythonUnittestsIncludeIndentedCommand(sublime_plugin.TextCommand):
    def run(self, view):
        fileName = self.view.file_name()
        instance = create_tests_wrapper(fileName, False, True)
        sublime.active_window().open_file(instance.unittestFilePath)


class CreatePythonUnittestsIncludeCommentedAndIndentedCommand(sublime_plugin.TextCommand):
    def run(self, view):
        fileName = self.view.file_name()
        instance = create_tests_wrapper(fileName, True, True)
        sublime.active_window().open_file(instance.unittestFilePath)
