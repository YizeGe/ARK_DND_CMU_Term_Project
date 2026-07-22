from cmu_graphics import *
from PIL import Image
import os
import random
import time

from combat import resolveAttack, updateBattleStatus, updateCharSeq, updateTurnPhase, enemyAttack
from Button import Button
from unit import Unit
from skill import Skill
from assets import load_char_actions, importActionPic, ACTION_DIR


def fitSkill(app,skill,unit):
    skill.damage=random.randint(1,4+unit.level//2)+unit.calculateBonus(unit.strength)

def onAppStart(app):
    #游戏状态
    app.units=[]
    app.width=1200
    app.height=800
    app.battleState=None

    #角色大小设置
    app.charWidth=app.width//5
    app.charHeight=app.width//5

    #定义角色行动顺序列表
    app.charActSeq=[]
    app.turn_index=0

    #当前角色阶段
    app.turn_phase=None
    app.selected_target=None

    #定义技能和按钮
    #posX,posY,width,height,text
    attackbutton=Button(None,None,None,None,'regular attack')
    #name,level,damage,time,button
    regular_attack=Skill('regular attack','act',None,1,attackbutton,'attack')

    #定义角色动作序列帧列表

    mizuki_frame_counts = {"attack": 43, "skill": 40, "idle": 260, "die": 30, "move": 40}
    mizuki_skills=[regular_attack]
    mizuki_action = load_char_actions(app, ACTION_DIR, 'mizuki_animations', 'mizuki_game_skin', 'mizuki', mizuki_frame_counts)

    texas_frame_counts = {"attack": 28, "skill": 28, "idle": 80, "die": 30, "move": 40}
    texas_skills=[regular_attack]
    texas_action = load_char_actions(app, ACTION_DIR, 'texas_animations', 'texas_time_skin', 'texas', texas_frame_counts)

    sog_frame_counts = {"attack": 70, "move": 20, "idle": 30, "die": 30}
    sog_skills=[regular_attack]
    sog_action = load_char_actions(app, ACTION_DIR, 'sog_animations', 'sog_re_skin', 'sog', sog_frame_counts)

    #创建角色

                    #app,name,team,occupation,x,y,atkRange,act,level
                    #力量，    敏捷，      智力，        感知，     体质，        魅力
                    #,strength,dexterity,intellegence,perception,constitution,charisma,
                    #action,skills):
    app.units.append(Unit(app,'水月','hero','战士',200,200,200,1,1,13,13,15,10,10,10,mizuki_action,mizuki_skills))
    app.units.append(Unit(app,'德克萨斯','hero','游荡者',200,600,200,1,1,12,15,13,10,10,10,texas_action,texas_skills))
    app.units.append(Unit(app,'雪犬A','enemy','游荡者',800,600,200,1,1,12,1,13,10,10,10,sog_action,sog_skills))
    # app.units.append(create_unit("地精A", "enemy",'游荡者', 600, 150, 6, 12, 1, 2))
    # app.units.append(create_unit("地精B", "enemy",'游荡者',720, 220, 6, 12, 1, 2))

    #角色序列帧索引定位
    app.step_count=0

    #初始化顺序列表
    updateCharSeq(app)

    #创建结束回合按钮
    app.endButton=Button(app.width-200,app.height-50,200,50,'End Round')

    #初始化每个角色的攻击伤害
    for unit in app.units:
        skills=unit.skills
        for skill in skills:
            fitSkill(app,skill,unit)


#轮到我方角色时，选择一名角色对其使用攻击（现在只有攻击）
def onMousePress(app,mouseX,mouseY):
    if app.battleState is None:
        if app.turn_phase != 'waiting_for_target':
            return
        curr_unit=app.charActSeq[app.turn_index]
        if curr_unit.state!='idle':
            return
        
        if app.endButton.clickOnButton(mouseX,mouseY):
            updateTurn(app,curr_unit)
            return

        clicked_unit=None
        for unit in app.units:
            if unit.alive and unit.clickOnCharacter(mouseX,mouseY):
                clicked_unit=unit
                break
        if clicked_unit is not None:
            dx = clicked_unit.x - curr_unit.x
            dy = clicked_unit.y - curr_unit.y
            dist = (dx**2 + dy**2) ** 0.5
            print(dist)
            if dist <= curr_unit.atkRange and curr_unit.act > 0:
                app.selected_target = clicked_unit
                curr_unit.act-=1
                curr_unit.updateMotion('attack')
                resolveAttack(app,curr_unit)
        else:
            curr_unit.startMove(mouseX,mouseY)

def onMouseMove(app,mouseX,mouseY):
    app.endButton.mouseOnButton(mouseX,mouseY)

def updateTurn(app,curr_unit):
    app.turn_index+=1
    if app.turn_index>=len(app.charActSeq):
        app.turn_index=0
    curr_unit.ap=curr_unit.maxAp
    curr_unit.act=curr_unit.maxAct

#重复播放角色动作图片，绘制角色
def drawCharacterMotion(app,unit):
    if len(unit.frames)>0:
        if unit.isDied() and unit.state!='die':
            unit.updateMotion('die')

        actList=unit.frames[unit.state]
        if len(actList)>0:
            if unit.state=='idle':
                unit.frameIndex=(unit.frameIndex+1)%len(actList)
            elif unit.state=='move':
                dx = unit.moveTargetX - unit.x
                dy = unit.moveTargetY - unit.y
                dist = (dx**2 + dy**2) ** 0.5
                speed = 8  # 每帧移动的像素数,可以自己调
                if dist < speed:
                    # 已经足够接近,直接落到目标点,结束移动
                    unit.x = unit.moveTargetX
                    unit.y = unit.moveTargetY
                    unit.state = 'idle'
                    unit.frameIndex = 0
                else:
                    # 按方向比例移动一步
                    unit.x += speed * dx / dist
                    unit.y += speed * dy / dist
                    # 同时推进move动作的帧,循环播放
                    unit.frameIndex = (unit.frameIndex+1) % len(actList)
            else:
                if unit.frameIndex >= len(actList) - 1:
                    resolveAttack(app,unit)
                    unit.state = 'idle'
                    unit.frameIndex = 0
                    if unit.team=='enemy':
                        updateTurn(app,unit)
                else:
                    unit.frameIndex += 1


def drawAp(app):
    unit=app.charActSeq[app.turn_index]
    length=200
    x=app.endButton.posX
    y=app.endButton.posY-20
    aplen=length-(unit.maxAp-unit.ap)
    drawRect(x,y,length,20,fill='gray')
    drawRect(x,y,aplen,20,fill='blue',border='black')

def onStep(app):
    app.step_count+=1
    for unit in app.units:
        drawCharacterMotion(app,unit)
        if unit.state=='move':
            unit.ap-=2
    updateBattleStatus(app)
    if app.battleState is not None:
        return
    updateCharSeq(app)
    updateTurnPhase(app)
    enemyAttack(app,app.charActSeq[app.turn_index])

def hpBarWidth(app,unit):
    hpbar=app.charWidth//2-app.charWidth//2//unit.maxHp*(unit.maxHp-unit.hp)
    if hpbar<=0:
        hpbar=1
    return hpbar

def redrawAll(app):
    for unit in app.units:
        if len(unit.frames[unit.state])>0:
            actList=unit.frames[unit.state]
            if len(actList)>0:
                curr_pic=actList[unit.frameIndex]
                drawImage(curr_pic,unit.x,unit.y,align='center',width=app.charWidth,height=app.charHeight)
                drawRect(unit.x-app.charWidth//2+50,unit.y+app.charHeight//2-50,app.charWidth//2,15,fill='gray')
                drawRect(unit.x-app.charWidth//2+50,unit.y+app.charHeight//2-50,hpBarWidth(app,unit),15,fill=unit.color)
                if unit is app.charActSeq[app.turn_index] and app.battleState is None:
                    drawRect(unit.x-app.charWidth//2,unit.y-app.charHeight//2,app.charWidth,app.charHeight,fill=None,border='navy')
    if app.battleState=='win':
        drawLabel('You Win!',app.width//2,app.height//2,font='sans',size=50,fill='red')
    elif app.battleState=='lose':
        drawLabel('You Lose...',app.width//2,app.height//2,font='sans',size=50,fill='gray')
    app.endButton.drawButton()
    drawAp(app)
        


def main():
    print("hello! Here's Gaizer's channel")
    runApp()

if __name__ == '__main__':
    main()