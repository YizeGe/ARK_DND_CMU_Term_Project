from cmu_graphics import *
import random

def updateCharSeq(app):
    app.charActSeq=[]
    for unit in app.units:
        if unit.alive:
            app.charActSeq.append(unit)


#判断战斗是否结束
def updateBattleStatus(app):
    charTeam=[]
    for unit in app.units:
        if unit.alive:
            charTeam.append(unit.team)
    if 'enemy' not in charTeam:
        app.battleState='win'
    elif 'hero' not in charTeam:
        app.battleState='lose'
    else:
        app.battleState=None

#敌人攻击目标设置为距离最近的hero
def enemyFindTarget(app,enemy):
    smallestDist=app.width*app.height
    target=None
    for unit in app.units:
        if unit.team=='hero' and unit.alive:
            dist=enemy.getDistance(unit.x,unit.y)
            if smallestDist>=dist:
                smallestDist=dist
                target=unit
    return target
    
#敌人自动往目标角色方向移动
def enemyApproach(app,enemy,target):
    if enemy.getDistance(target.x,target.y)>enemy.skills[0].range:
        dx=target.x-enemy.x
        dy=target.y-enemy.y
        dist=enemy.getDistance(target.x,target.y)
        percentage=(dist-150)/dist
        x=dx*percentage+enemy.x
        y=dy*percentage+enemy.y
        enemy.startMove(x,y)


#敌人回合自动攻击（等待制作复杂敌人意图）
def enemyAttack(app,enemy):
    if enemy.team=='enemy' and enemy.state=='idle':
        if enemy.act>0:
            app.selected_target=enemyFindTarget(app,enemy)
            dist=enemy.getDistance(app.selected_target.x,app.selected_target.y)
            if dist>enemy.skills[0].range:
                enemyApproach(app,enemy,app.selected_target)
            else:
                enemy.updateMotion('attack')
                enemy.act-=1

#更新当前游戏角色对应状态
def updateTurnPhase(app):
    if app.charActSeq[app.turn_index].team=='hero':
        app.turn_phase='waiting_for_target'
    else:
        app.turn_phase='enemy_acting'

#角色回合轮换
def updateTurn(app,curr_unit):
    app.turn_index+=1
    if app.turn_index>=len(app.charActSeq):
        app.turn_index=0
    curr_unit.ap=curr_unit.maxAp
    curr_unit.act=curr_unit.maxAct

#判断当前角色是否能够进行攻击，并返回攻击目标
def canPlayerAct(app):
    if not app.battleState is None:
        return
    if app.turn_phase!='waiting_for_target':
        return
    unit=app.charActSeq[app.turn_index]
    if unit.state!='idle':
        return
    return unit

#如果存在，返回被点击的角色，否则返回None
def findClickedCharacter(app,mouseX,mouseY):
    for unit in app.units:
        if unit.clickOnCharacter(mouseX,mouseY):
            return unit
    return None

#尝试进行攻击并更新角色资源
def tryAttackUnit(app,attacker,target):
    dist=attacker.getDistance(target.x,target.y)
    if dist>attacker.skills[0].range:
        return
    if attacker.act<=0:
        return
    app.selected_target=target
    attacker.act-=1
    attacker.updateMotion('attack')

def resolveAttack(app,attacker):
    if app.selected_target is None:
        return
    if app.selected_target.isDied():
        return
    skill=attacker.skills[0]
    if skill.isHit(app.selected_target.ac):
        damage=skill.calDamage(attacker)
        app.selected_target.hp-=damage
        if app.selected_target.isDied():
            print(f'{app.selected_target.name} is died!')
    else:
        print('miss!')
