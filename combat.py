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
    
    damage=attacker.skills[0].attack(app.selected_target)
    app.selected_target.hp-=damage
    
    print(app.selected_target,target.hp)

    app.selected_target = None


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
                app.selected_target=u
        unit.updateMotion('attack')


def updateTurnPhase(app):
    if app.charActSeq[app.turn_index].team=='hero':
        app.turn_phase='waiting_for_target'
    else:
        app.turn_phase='enemy_acting'

def updateTurn(app,curr_unit):
    app.turn_index+=1
    if app.turn_index>=len(app.charActSeq):
        app.turn_index=0
    curr_unit.ap=curr_unit.maxAp
    curr_unit.act=curr_unit.maxAct