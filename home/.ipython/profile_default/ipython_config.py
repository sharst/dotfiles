#!/usr/bin/env python
from IPython.terminal.prompts import Prompts, Token

# Configuration file for ipython.

c = get_config()

# Execute the given command string.
# c.InteractiveShellApp.code_to_run = ''

# lines of code to run at IPython startup.
# c.InteractiveShellApp.exec_lines = []

# List of files to run at IPython startup.
# c.InteractiveShellApp.exec_files = []
# c.TerminalIPythonApp.module_to_run = ''

# lines of code to run at IPython startup.
c.TerminalIPythonApp.exec_lines = ["import pylab as plt",
                                   "import numpy as np",
                                   "import datetime",
                                   "import pytz"]

c.TerminalInteractiveShell.deep_reload = False

# Automatically call the pdb debugger after every exception.
c.TerminalInteractiveShell.pdb = False


class SimplePrompts(Prompts):
    def in_prompt_tokens(self, cli=None):
        return [
            (Token.Prompt, u' >>> '),
        ]

    def continuation_prompt_tokens(self, cli=None, width=None):
        if width is None:
            width = self._width()
        return [
            (Token.Prompt, (' ' * (width - 2)) + ">"),
        ]

    def out_prompt_tokens(self):
        return [
            (Token.Prompt, u' <<< '),
        ]

#  Use IPython v5+ new API:
c.TerminalInteractiveShell.prompts_class = SimplePrompts
