from blocks import *
from flowgraph import *
from basicblock import *
from redundantLoadStore import *
from redundantLabels import *
from copyPropagation import *
from subprocess import call

readfile = "O0/pi.s"
writefile = "copyproptimized.s"

myBlock = blockBuilder(readfile)
myBlock.analyze()
myBlock.findBlockTargets()

opt = copyPropagation(myBlock.basicBlocks)
opt.analyseBlocks()

buffer = ""

for block in opt.optimizedBlocks:
    for operation in block.operations:
        if operation.included:
            buffer += operation.code + "\n"
        else:
            buffer += "# " + operation.code + "\n"

    #buffer += "\n## basicblock ##\n\n"

f = open(writefile, 'w')
f.write(buffer)

call(["gvim", "-d", readfile, writefile])
