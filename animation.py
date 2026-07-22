from combat import resolveAttack, updateTurn
from cmu_graphics import *

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
    attackLen=len(unit.frames['attack'])
    if unit.frameIndex>=attackLen-1:
        unit.frameIndex=0
        return True
    unit.frameIndex+=1
    return False

def updateSkillAnimation(unit):
    skillLen=len(unit.frames['skill'])
    if unit.frameIndex>=skillLen-1:
        unit.frameIndex=0
        return True
    unit.frameIndex+=1
    return False

def updateAnimation(app,unit):
    isAttack,isSkill=False,False
    if unit.isDied():
        if unit.state!='die':
            unit.frameIndex=0
            unit.updateMotion('die')
        updateDieAnimation(unit)
    elif unit.isMoving():
        updateMoveAnimation(unit)
        unit.moveCharacter()
        unit.ap-=2
    if unit.state=='idle':
        updateIdleAnimation(unit)
    if unit.state=='attack':
        isAttack=updateAttackAnimation(unit)
    if unit.state=='skill':
        isSkill=updateSkillAnimation(unit)
    if isAttack or isSkill:
        resolveAttack(app,unit)
        unit.updateMotion('idle')
        if unit.team=='enemy':
            updateTurn(app,unit)

    
