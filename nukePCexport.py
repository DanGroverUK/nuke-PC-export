# Written by Dan Grover, dan-grover@dan-grover.com If you have any comments,
# bugs, suggestions, questions, whatever - please email me!

#   v8.0        The CLI and GUI are now separate, so they'll have separate
#               version numbers going forwards.
#   v7.0-cli    An alternative to the normal one that works on deadline
#   v7.0        I'm now setting the version number to 7.0 and using boring old
#               semantic versioning. It's also now added to git and Pep-8'd.
#   v6.2        Changed it to a generator
#   v6.1        Changed from a while to a for loop, no more deleting items.
#   v6          Added data caching then writing in chunks.
#   v5          Original functionality at the time I joined TJ

import nuke
import subprocess
import sys


def genUI():
    pcPanel = nuke.Panel("PC Export - v8.0")
    pcPanel.addFilenameSearch("Output Location:", "")
    pyPath = ("\\\\files.taylorjames.com\\Library$\\"
              "Nuke\\python\\nuke-PC-export_cli.py")
    pcPanel.addFilenameSearch("Python Processing File:", pyPath)
    pcPanel.addButton("Cancel")
    pcPanel.addButton("Process Locally")
    ret = pcPanel.show()
    if ret == 1:
        print(ret)
        nukeLocation = sys.executable
        outputFolder = pcPanel.value("Output Location:")
        scriptLocation = pcPanel.value("Python Processing File:")
        nukeScriptLocation = nuke.root().knob('name').value()
        subprocess.Popen([nukeLocation,
                          "-t",
                          scriptLocation,
                          nukeScriptLocation,
                          outputFolder],
                          creationflags=subprocess.CREATE_NEW_CONSOLE)
    else:
        print "Closed!"


#vars = genUI()
