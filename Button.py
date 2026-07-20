from cmu_graphics import *

class Button:
    #初始化
    def __init__(self,posX,posY,width,height,text):
        self.posX=posX
        self.posY=posY
        self.text=text
        self.color='cyan'
        self.width=width
        self.height=height
    
    #检查是否在按钮中点击
    def clickOnButton(self,mouseX,mouseY):
        left=self.posX
        right=self.posX+self.width
        up=self.posY
        down=self.posY+self.height
        return left<=mouseX<=right and up<=mouseY<=down
    
    #鼠标悬浮时改变颜色
    def mouseOnButton(self,mouseX,mouseY):
        if self.clickOnButton(mouseX,mouseY):
            self.color='navy'
        else:
            self.color='cyan'

    #绘制按钮（有点简陋）
    def drawButton(self):
        drawRect(self.posX,self.posY,self.width,self.height,fill=self.color)
        drawLabel(self.text,self.posX+self.width/2,self.posY+self.height/2,size=20,fill='red')