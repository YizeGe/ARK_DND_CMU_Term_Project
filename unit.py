from cmu_graphics import *
import math

class Unit:
    def __init__(self,app,name,team,occupation,
                 x,y,atkRange,act,level
                 #力量，    敏捷，      智力，        感知，     体质，        魅力
                 ,strength,dexterity,intellegence,perception,constitution,charisma,
                 action,skills):
        self.name=name
        self.team=team
        self.occupation=occupation
        self.x=x
        self.y=y
        self.moveTargetX=None
        self.moveTargetY=None
        self.atkRange=atkRange
        self.maxHp=level*constitution
        self.hp=level*constitution
        self.maxAp=10*dexterity
        self.ap=10*dexterity
        self.maxAct=act
        self.act=act
        self.ac=dexterity
        self.level=level
        self.strength=strength
        self.dexterity=dexterity
        self.intellegence=intellegence
        self.perception=perception
        self.constitution=constitution
        self.charisma=charisma
        self.alive=True
        self.color="dodgerBlue" if team == "hero" else "crimson"
        self.frames=action
        self.state='idle'
        self.frameIndex=0
        self.clickRadius=app.charHeight
        self.skills=skills

    #检查角色是否被点击
    def clickOnCharacter(self,mouseX,mouseY):
        x,y=self.x,self.y
        dis=((x-mouseX)**2+(y-mouseY)**2)**0.5
        if dis<self.clickRadius//4:
                return True
        return False
    
    #判断角色开始移动并更新目的地
    def startMove(self,targetX,targetY):
        if self.ap <= 0:
            return
        self.moveTargetX = targetX
        self.moveTargetY = targetY
        self.updateMotion('move')

    #更新角色动作
    def updateMotion(self,motionState):
        self.state=motionState
        self.frameIndex=0
    
    def calculateBonus(self, feature):
        return math.floor((feature-10)/2)
    
    def __repr__(self):
         return f'<{self.team}, {self.name}>'