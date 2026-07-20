from cmu_graphics import *
import random

def updateCharSeq(app):
    app.charActSeq=[]
    for unit in app.units:
        if unit.alive:
            app.charActSeq.append(unit)


#攻击伤害结算和更新
def resolveAttack(app,attacker):
    if app.selected_target is None:
        return
    target=None
    for unit in app.units:
        if unit==app.selected_target:
            target=unit
            break
    if target is None or not target.alive:
        app.selected_target=None
        return
    
    attacker.skills[0].attack(app.selected_target)
    
    print(app.selected_target,target.hp)

    app.selected_target = None


def reAttack(app,target):
    skillName='regular_attack'


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


    #敌人回合自动攻击（等待制作复杂敌人意图）
def enemyAttack(app,unit):
    if unit.team=='enemy' and unit.state=='idle':
        for u in app.units:
            if u.alive and u.team=='hero':
                app.selected_target=u.name
        unit.updateMotion('attack')


def updateTurnPhase(app):
    if app.charActSeq[app.turn_index].team=='hero':
        app.turn_phase='waiting_for_target'
    else:
        app.turn_phase='enemy_acting'