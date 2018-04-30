# Written by Dan Grover, dan-grover@dan-grover.com If you have any comments,
# bugs, suggestions, questions, whatever - please email me!

#   v7.1-cli    Altered version that'll get re-branched into the main
#   v7.0-cli    An alternative to the normal one that works on deadline
#   v7.0        I'm now setting the version number to 7.0 and using boring old
#               semantic versioning. It's also now added to git and Pep-8'd.
#   v6.2        Changed it to a generator
#   v6.1        Changed from a while to a for loop, no more deleting items.
#   v6          Added data caching then writing in chunks.
#   v5          Original functionality at the time I joined TJ

import nuke
import threading
import timeit
import cStringIO
import os

# A generator function that returns the next whitespace split
# entry in a string. Perfect for getting the next value from
# the nuke nobs.

def genUI():
    pcPanel = nuke.Panel("PC Export - v7.1")
    pcPanel.addFilenameSearch("Output Location:", "")
    pcPanel.addButton("Cancel")
    pcPanel.addButton("Process Locally")
    pcPanel.addButton("Process on Deadline")
    ret = pcPanel.show()
    if ret == 1:
        print(ret)
        fileLocation = pcPanel.value("Output Location:")
        commandString = " ".join(["\"C:\\Program Files\\Nuke11.0v2\\Nuke11.0.exe\"",
                                  "-t",
                                  "\"C:\\git\\nuke-PC-export\\nuke-PC-export_cli.py\"",
                                  ("\"" + nuke.root().knob('name').value() + "\""),
                                  ("\"" + fileLocation + "\"")])
        print(commandString)
        # if not (fileLocation.endswith(".csv")):
        #     fileLocation = fileLocation + ".csv"
        # threading.Thread(None, writeFile(fileLocation)).start()
        # writeFile(fileLocation)
    else:
        print "Closed!"


vars = genUI()
# print(sys.argv)
# nuke.scriptSource(sys.argv[1])
# for a in nuke.allNodes():
#     if a.Class() == 'BakedPointCloud' and a['disable'].getValue() == 0.0:
#         print a['name'].getValue()
#         outFile = "".join([sys.argv[2], "\\", a['name'].getValue(), ".csv"])
#         writeFile(a, outFile)
#         print("Output successfully written to: {outFile}".format(outFile=outFile))