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
        return False
    return True

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
    #如果死了
    if unit.isDied():
        dieLen=len(unit.frames['die'])
        if unit.state!='die':
            unit.frameIndex=0
            unit.updateMotion('die')
        if unit.frameIndex>=dieLen-1:
            return False
        if updateDieAnimation(unit):
            return True
    #如果在动
    elif unit.isMoving():
        updateMoveAnimation(unit)
        unit.moveCharacter()
        unit.ap-=2
    #如果什么都不干
    if unit.state=='idle':
        updateIdleAnimation(unit)
    #如果在攻击
    if unit.state=='attack':
        isAttack=updateAttackAnimation(unit)
    #如果在放技能
    if unit.state=='skill':
        isSkill=updateSkillAnimation(unit)
    #如果攻击或者技能结束
    if isAttack or isSkill:
        unit.state='idle'
        return True
    return False

    
