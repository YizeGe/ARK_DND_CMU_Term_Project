def updateIdleAnimation(unit):
    idleLen=len(unit.frames['idle'])
    if idleLen==0:
        return
    unit.frameIndex=(unit.frameIndex+1)%idleLen

def updateDieAnimation(unit):
    dieLen=len(unit.frames['die'])
    if unit.frameIndex<dieLen-1:
        unit.frameIndex+=1

def updateMoveAnimation(unit):
    moveLen=len(unit.frames['move'])
    if unit.isMoving():
        unit.frameIndex=(unit.frameIndex+1)%moveLen

def updateAttackAnimation(unit):
    attackLen=unit.frames[unit.state]
    if unit.frameIndex>=attackLen-1:
        return True
    unit.frameIndex+=1
    return False

def updateMotion(unit):
    if unit.isDied():
        updateDieAnimation(unit)
    elif unit.isMoving():
        updateMoveAnimation(unit)
