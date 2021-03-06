from operations_new import *
from optimizationClass import *

class redundantLabels(optimizationClass):
    def __init__(self, blocks):
        """
        Initializes all the necessary variables.
        """
        
        self.name            = "Remove redundant labels / jumps"
        self.output          = []
        self.optimizedBlocks = blocks


    def analyseBasicBlock(self, block):
        """
        Look at a single basic block and its target. If the target only has two
        operations, of which the last is a control operation, make the block
        jump to end directly.
        """

        if not block.target == None and block.target.numOperations() == 2:
            if block.target.operations[-1].type == operation.CONTROL:
                target = block.target.operations[-1].getTarget()
            else:
                raise Exception, "Basicblock has no control operation on the\
                    last line!"
            
            if target[0] == "$" and \
                block.operations[-1].type == operation.CONTROL:
                    block.operations[-1].setTarget(target)
                    
                    # Exclude the old block from the code.
                    block.target.exclude()
                    block.target = block.target.target
                

    def getRedundantLabels(self, block):
        if not (block.target == None) and len(block.target.code) == 2:
            #Replace jump target with target of the target-block
            print block.getLabel() + " points to " + \
                block.target.getLabel() + " with " + \
                str(len(block.target.code)) + " lines:"
            print block.target.code
