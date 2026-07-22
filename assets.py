import os
from cmu_graphics import *
from PIL import Image


#主程序文件地址
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#角色素材文件地址
ACTION_DIR = os.path.join(BASE_DIR, 'action')

#寻找角色动作文件地址并返回动作字典
def load_char_actions(app, action_dir, char_folder, skin_folder, char_action, frame_counts):
    actions = {}
    for action_name, pic_count in frame_counts.items():
        path = os.path.join(action_dir, char_folder, skin_folder, f"{char_action}_{action_name}")
        actions[action_name] = importActionPic(app, pic_count, path)
    return actions

#返回角色动作列表
def importActionPic(app,picNum,filePath):
    action_list=[]
    for i in range(picNum):
        path=f'{filePath}/frame_{i:03d}.png'
        action_list.append(CMUImage(Image.open(path)))
    return action_list