from translation import *
from basicblock import *

#
# TODO
# 
# The code for storing each start line of a basicblock is not really needed
# anymore, but could prove useful with debugging.
#
# The targets should not just be line numbers, but should become blocks.
#
# --
#
# Possible optimization:
# Find basic blocks by following the basic blocks.
#   - don't read the next line after a jump, but continue from the line of the
#     jump target. This way only reachable code is processed.
#

class blockBuilder:
    """
    This class provides functionality for splitting a piece of assembly code
    into basicblocks.
    """

    def __init__(self, filename):
        """
        Constructor.

        Loads a file with assembly code and reads every line. Each line is
        stored in a list.
        """

        self.file    = open(filename)
        self.listing = self.file.readlines()
        self.basicBlocks = [] 
        self.newblock    = 1


    def analyze(self):
        """
        Method that analyses the assembly code on each line and begins or ends a
        basicblock depending on what code is on the current line.
        """

        lineNumber = 0
        self.startPoints = []
        currentBlock = None;
        numBlocks = 0

        # Iterate over every line of assembly stored in this object. 
        for line in self.listing:
            try:
                operator = getOp(line)
            except:
                " Nothing to do: no operator on this line "
            else:
                # Create a new block if we previously found a control operator
                # or if we're in the first block.
                if self.newblock == 1:
                    numBlocks += 1
                    currentBlock = basicBlock(line, "B" + str(numBlocks))
                    self.newblock = 0

                    self.basicBlocks.append(currentBlock)
                else:
                    #cut the last character off line - it's a "newline" char
                    currentBlock.addLine(line[:len(line)-1])

                # Check if we found a jump or branch operator.
                if isControl(operator):

                    # Jump or branch operator: end of block
                    self.startPoints.append(lineNumber + 2)
                    self.newblock = 1

                    # Target will be start of new block
                    target = getJumpTarget(line)

                    try:
                        position = self.getLabelPosition(target)
                    except:
                        " Nothing to do: the label position is not in current file "
                    else:
                        self.startPoints.append(position)

            lineNumber += 1

        # Remove duplicates and sort list
        self.startPoints = list(set(self.startPoints))
        self.startPoints.sort()


    def getLabelPosition(self, target):
        """
        Method for finding the line a jump target can be found.
        """

        lineNumber = 0

        # Look for labels of the form: '$name'
        if target[0] == "$" :

            for line in self.listing:
                if len(line) - 2 > len(target) or len(line) < len(target):
                    " Target not on this line, skipping. "
                elif line[0:len(line)-2] == target:
                    return lineNumber

                lineNumber += 1

        # Look for labels of the form: '__name'
        elif target[0:2] == "__" :

            for line in self.listing:
                if line[0:len(line)-1] == target[2:len(line)-1]:
                    return lineNumber

                lineNumber += 1

        raise Exception, "Label not in current file."

    
    def getBlockTargets(self):
        """
        Find the operational successor of each basic block.
        """
        for block in self.basicBlocks:
            target = getJumpTarget(block.getTarget())

            for searchBlock in self.basicBlocks:
                label = searchBlock.getLabel()

                if target == label[0:len(label) - 2] or target[2:len(label) - 1] == label[0:len(label) - 1]:
                    block.addTarget(searchBlock)
                    break
