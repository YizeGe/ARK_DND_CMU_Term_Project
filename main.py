from cmu_graphics import *
from PIL import Image as PILImage
import os
import random
import time

from combat import *
from animation import updateAnimation
from button import Button
from character import *
from game_state import game_state


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

    #创建角色
    app.units.append(createHero('水月'))
    app.units.append(createHero('德克萨斯'))
    app.units.append(createEnemy('sog','雪犬A',600,600))

    #角色序列帧索引定位
    app.step_count=0

    #初始化顺序列表
    updateCharSeq(app)

    #创建结束回合按钮
    app.endButton=Button(app.width-200,app.height-50,200,50,'End Round')



#轮到我方角色时，选择一名角色对其使用攻击（现在只有攻击）
def onMousePress(app,mouseX,mouseY):
    curr_unit=canPlayerAct(app)
    if curr_unit is None:
        return
    if app.endButton.clickOnButton(mouseX,mouseY):
        updateTurn(app,curr_unit)
        return
    clicked_unit=findClickedCharacter(app,mouseX,mouseY)
    if not clicked_unit is None:
        tryAttackUnit(app,curr_unit,clicked_unit)
    else:
        curr_unit.startMove(mouseX,mouseY)
    

def onMouseMove(app,mouseX,mouseY):
    app.endButton.mouseOnButton(mouseX,mouseY)



def drawAp(app):
    unit=app.charActSeq[app.turn_index]
    length=200
    x=app.endButton.posX
    y=app.endButton.posY-20
    aplen=max(length*unit.ap/unit.maxAp,1)
    drawRect(x,y,length,20,fill='gray')
    drawRect(x,y,aplen,20,fill='blue',border='black')

def onStep(app):
    app.step_count+=1
    checkDied(app)
    for unit in app.units:
        if updateAnimation(app,unit):
            resolveAttack(app,unit)
            if unit.team=='enemy':
                updateTurn(app,unit)
    updateBattleStatus(app)
    if app.battleState in (game_state.BATTLE_LOSE,game_state.BATTLE_WIN):
        return
    if app.turn_index>=len(app.charActSeq):
        app.turn_index=0
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
                if unit.facing=='left':
                    curr_pic=CMUImage(curr_pic.image.transpose(PILImage.FLIP_LEFT_RIGHT))
                drawImage(curr_pic,unit.x,unit.y,align='center',width=app.charWidth,height=app.charHeight)
                drawRect(unit.x-app.charWidth//2+50,unit.y+app.charHeight//2-50,app.charWidth//2,15,fill='gray')
                drawRect(unit.x-app.charWidth//2+50,unit.y+app.charHeight//2-50,hpBarWidth(app,unit),15,fill=unit.color)
                if app.battleState not in (game_state.BATTLE_LOSE,game_state.BATTLE_WIN) and unit is app.charActSeq[app.turn_index]:
                    drawRect(unit.x-app.charWidth//2,unit.y-app.charHeight//2,app.charWidth,app.charHeight,fill=None,border='navy')
    if app.battleState==game_state.BATTLE_WIN:
        drawLabel('You Win!',app.width//2,app.height//2,font='sans',size=50,fill='red')
    elif app.battleState==game_state.BATTLE_LOSE:
        drawLabel('You Lose...',app.width//2,app.height//2,font='sans',size=50,fill='gray')
    app.endButton.drawButton()
    drawAp(app)
        


def main():
    print("hello! Here's Gaizer's channel")
    runApp()

if __name__ == '__main__':
    main()