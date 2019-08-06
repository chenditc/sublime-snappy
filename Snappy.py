# -*- coding: utf-8 -*-

import sublime
import sublime_plugin

import os
import subprocess


"""
Snappy package for Sublime Text

"""


COMMAND_NOT_FOUND_MSG = "!!! Make sure 'python-snappy' lib is installed !!!\n"
COMMAND_LINE = "python3 -m snappy -d {0}"


def run_command(command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return iter(p.stdout.readline, b'')


class SnappyCommand(sublime_plugin.TextCommand):
    def run(self, edit, filename=None):
        if filename is None or not filename.endswith('.snappy'):
            return

        pos = 0
        command = COMMAND_LINE.format(filename).split()

        try:
            for line in run_command(command):
                pos += self.view.insert(edit, pos, line.rstrip().decode("utf-8") + "\n")
            # TODO: future improve, use native decompression method
            #from snappy import snappy_formats
            #from io import BytesIO
            #method, read_chunk = snappy_formats.get_decompress_function(snappy_formats.DEFAULT_FORMAT, open(filename, "rb"))
            #result_buffer = BytesIO()
            #method(open(filename, "rb"), result_buffer)
            #result = result_buffer.getvalue().decode("utf-8")
            #for line in result.split("\n"):
            #   pos += self.view.insert(edit, pos, line.rstrip() + "\n")
        except FileNotFoundError:
            pos += self.view.insert(edit, pos, COMMAND_NOT_FOUND_MSG)

        self.view.set_name(os.path.basename(filename))
        self.view.set_read_only(True)


class OpenSnappyFile(sublime_plugin.EventListener):
    def on_load(self, view):
        filename = view.file_name()
        if filename.endswith('.snappy'):
            sublime.status_message("opening snappy file: " + filename)
            print("opening snappy file: " + filename)
            snappy_view = view.window().new_file()
            view.close()
            snappy_view.run_command('snappy', {'filename': filename})
