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

# Output prompt. '\#' will be transformed to the prompt number
# c.PromptManager.out_template = 'Out[\\#]: '
c.PromptManager.out_template = '< '

# Continuation prompt.
# c.PromptManager.in2_template = '   .\\D.: '

# Input prompt.  '\#' will be transformed to the prompt number
#c.PromptManager.in_template = 'In [\\#]: '
c.PromptManager.in_template = '> '

