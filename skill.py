from cmu_graphics import *
import random
import Button

class Skill:
    #初始化技能
    def __init__(self,name,level,damage,time,button,effect):
        self.name=name
        self.level=level
        self.damage=damage
        self.time=time
        self.button=button
        self.effect=effect

    def isHit(self,ac):
        roll=self.rollDice()
        if roll>ac:
            return True
        else:
            return False

    def returnEffect(self,attacker,target):
        if self.isHit(target.ac):
            if self.effect=='attack':
                target.hp-=attacker.calculateBonus(attacker.strength)

    def rollDice(self):
        return random.randint(1,20)
    
    def drawButton(self,x,y,width,height):
        fill,text=self.button.color,self.button.text
        drawRect(x,y,width,height,fill=fill,border='black')
        drawLabel(text,x+width/2,y+height/2,fill='black',size=width//10)
