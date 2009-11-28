class basicBlock:
    """
    Represents a basic block
    """
    code    = []
    targets = []
    genSet  = []
    killSet = []
    labels  = []
    name    = None

    def __init__(self, name, startLine):
        """
        Initialises all class variables.
        """
        self.name       = name
        self.startLine  = startLine

        self.code       = []
        self.targets    = []
        self.genSet     = []
        self.killSet    = []
        self.labels     = []


    def addLine(self, line):
        """
        Method for adding a line to the lines of code inside this basicblock.
        """

        self.code.append(line)


    def getLine(self, lineNumber):
        """
        Returns a line of code, using the global line number, not the line
        number within the block.
        """

        return self.code[lineNumber - self.startLine]


    def addTarget(self, targetNode):
        """
        Method for adding a target to which this basicblock can jump at the end
        of its execution.
        """

        self.targets.append(targetNode)

    
    def addGen(self, lineNumber):
        """
        Appends a linenumber to the gen list.
        """

        self.genSet.append(lineNumber)


    def addKill(self, lineNumber):
        """
        Appends a linenumber to the kill list.
        """

        self.killSet.append(lineNumber)


    def getLabel(self):
        """
        Return the name / label of this basicblock.
        """

        return self.name


    def getTarget(self):
        """
        The last instruction of a basicblock is a branch or jump, so the target
        of the block will be on the last line.
        """

        return self.code[-1]
    

    def findLabel(self, label):
        """
        Constructs a list of all available labels within this basic block.
        """
        
        if label[0] == "$":
            for line in self.code:
                if line[0:-1] == label:
                    self.labels.append(label)
                    return True
        elif label[0:2] == "__":
            for line in self.code:
                if line[:-1] == label[2:]:
                    self.labels.append(label)
                    return True

        return False


    def hasLabel(self, label):
        """
        Check the list of available labels or look for a label over every line
        of code.
        """

        if label in self.labels:
            return True
        else:
            return self.findLabel(label)
                    
                
