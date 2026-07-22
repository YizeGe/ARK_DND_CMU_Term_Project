from cmu_graphics import *



def updateIdleAnimation(unit):
    idleLen=len(unit.frames['idle'])
    unit.frameIndex=(unit.frameIndex+1)%idleLen

def updateDieAnimation(unit):
    dieLen=len(unit.frames['die'])
    if unit.frameIndex<dieLen:
        unit.frameIndex+=1

def updateMoveAnimation(unit):
    idleLen=len(unit.frames['move'])
    if unit.isMoving():
        unit.frameIndex+=1
    else:
        unit.frameIndex=0

def updateAttackAnimation(app,unit):
