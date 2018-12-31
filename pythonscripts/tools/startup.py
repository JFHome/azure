#I use the following to enable history on python shell.
#This is my .pythonstartup file . PYTHONSTARTUP environment variable is set to this file path.
# python startup file 
import readline 
import rlcompleter 
import atexit 
import os 
# tab completion 
readline.parse_and_bind('tab: complete') 
# history file 
histfile = os.path.join(os.environ['HOME'], '.pythonhistory') 
try: 
    readline.read_history_file(histfile) 
except IOError: 
    pass 
atexit.register(readline.write_history_file, histfile) 
del os, histfile, readline, rlcompleter
#You will need to have the modules readline, rlcompleter to enable this.
#Check out the info on this at : http://docs.python.org/using/cmdline.html#envvar-PYTHONSTARTUP.


