import cPickle
from django.db import models
from mapping import MAPPING

class Block(models.Model):

    blockStr = models.TextField()
    
    @classmethod
    def createBlock(cls, blockType):
        block = MAPPING[blockType]()
        block.foldFunc()
        blockObj = cls(blockStr=cPickle.dumps(block))
        blockObj.save()
        return blockObj
    
    def getBlock(self):
        block = cPickle.loads(str(self.blockStr))
        block.unfoldFunc()
        return block

    def saveBlock(self, block):
        block.foldFunc()
        blockStr = cPickle.dumps(block)
        self.blockStr = blockStr
        self.save()

    @classmethod
    def collapseBlock(cls, block):
        block.foldFunc()
        blockObj = cls(blockStr=cPickle.dumps(block))
        blockObj.save()
        return blockObj
        
