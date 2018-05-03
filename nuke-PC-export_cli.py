# Written by Dan Grover, dan-grover@dan-grover.com If you have any comments,
# bugs, suggestions, questions, whatever - please email me!

#   v8.0        The CLI and GUI are now separate, so they'll have separate
#               version numbers going forwards.
#   v7.1-cli    Altered version that'll get re-branched into the main
#   v7.0-cli    An alternative to the normal one that works on deadline
#   v7.0        I'm now setting the version number to 7.0 and using boring old
#               semantic versioning. It's also now added to git and Pep-8'd.
#   v6.2        Changed it to a generator
#   v6.1        Changed from a while to a for loop, no more deleting items.
#   v6          Added data caching then writing in chunks.
#   v5          Original functionality at the time I joined TJ

import nuke
import timeit
import cStringIO

# A generator function that returns the next whitespace split
# entry in a string. Perfect for getting the next value from
# the nuke nobs.


def next_three(var1):
    stringpos = 0
    tempVar = ""
    while True:
        while var1[stringpos] != " ":
            tempVar = tempVar + var1[stringpos]
            stringpos += 1
        yield tempVar
        tempVar = ""
        stringpos += 1


def writeFile(node, fileOut):
    tic = timeit.default_timer()
    # if len(nuke.selectedNodes()) != 1:
    #     nuke.message("Exactly one BakedPointCloud node should be selected.")
    #     return

    # This string represents the XYZ positions
    xyzString = node.knob("serializePoints").getValue()
    # This string represents the RGB Colour
    rgbString = node.knob("serializeColors").getValue()
    # Create the .csv file
    csvString = fileOut
    # Open it for writing
    csvFile = open(csvString, 'w')
    # Find out the total number of points
    xyzGen = next_three(xyzString)
    rgbGen = next_three(rgbString)
    totalPoints = int(next(xyzGen))
    # We actually don't use the value below, but we need to get the first
    # generator value so that when we start getting the subsequent values,
    # we have the useless first value already out of the way.
    next(rgbGen)
    # Create a counter variable for use in the progress bar
    counter = 0
    # Create the IO String that the csv data is temporarily cached to
    writeString = cStringIO.StringIO()
    # Write the file headers that Krakatoa's PRT loader wants
    csvFile.write(
        "float32 Position[0], float32 Position[1], float32 Position[2],"
        " float16 Color[0], float16 Color[1], float16 Color[2]\n")
    # Create a new task for the threader to run.
    task = nuke.ProgressTask("Saving Data...")
    # Loop through the number of points, defined by the first return from
    # the generator functions
    for g in range(1, totalPoints):
        # Set up the cancel behaviour:
        if task.isCancelled():
            csvFile.close()
            nuke.executeInMainThread(nuke.message, args=("Aborted",))
            return
        # write out the line for this point
        lineToWrite = "{x},{y},{z},{r},{g},{b}\n".format(x=next(xyzGen),
                                                         y=next(xyzGen),
                                                         z=next(xyzGen),
                                                         r=next(rgbGen),
                                                         g=next(rgbGen),
                                                         b=next(rgbGen))
        writeString.write(lineToWrite)
        counter = counter + 1
        # Calculate the progress value.
        task.setProgress(int(100 * (float(counter) / float(totalPoints))))
        # Set a progress message.
        task.setMessage(("Caching point " + str(counter)))
        if (counter % 20000) == 0:
            toc = timeit.default_timer()
            processingTime = str(round((toc - tic), 1))
            print("Time to {} points: {}s - {}%".format(str(counter),
                                                        processingTime,
                                                        str(int(100 * (float(counter) / float(totalPoints))))))
    # Write the output
    print("Writing out .csv File...")
    csvFile.write(writeString.getvalue())
    writeString.close()
    # Close the file to save it.
    csvFile.close()

print(sys.argv)
print("Loading Script File...")
nuke.scriptSource(sys.argv[1])
for a in nuke.allNodes():
    if a.Class() == 'BakedPointCloud' and a['disable'].getValue() == 0.0:
        print a['name'].getValue()
        outFile = "".join([sys.argv[2], "\\", a['name'].getValue(), ".csv"])
        writeFile(a, outFile)
        print("Output successfully written to: {outFile}".format(outFile=outFile))