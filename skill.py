from cmu_graphics import *
import random
import Button

class Skill:
    #初始化技能
    def __init__(self,name,level,damage,time,button):
        self.name=name
        self.level=level
        self.damage=damage
        self.time=time
        self.button=button

    def attack(self,target):
        roll=self.rollDice()
        if roll>target.ac:
            if roll==20:
                self.damage*2
            return self.damage
        else:
            return None

    def rollDice(self):
        return random.randint(19,20)
    
    def drawButton(self,x,y,width,height):
        fill,text=self.button.color,self.button.text
        drawRect(x,y,width,height,fill=fill,border='black')
        drawLabel(text,x+width/2,y+height/2,fill='black',size=width//10)
