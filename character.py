#这个文件会储存所有的角色和技能的具体数据，并包含角色和技能创建函数
from cmu_graphics import *
from skill import Skill
from unit import Unit
from button import Button
from assets import *

ALL_SKILL_DATA={
    'regular_attack':{
        'name':'regular_attack',
        'button':None,
        'effect':'damage',
        'dice_count':1,
        'dice_sides':6,
        'fixed_damage':6,
        'hit_bonus':2,
        'is_ranged':False,
        'range':200,
        'cost_action':True,
        'cost_bonus':False,
        'cost_reaction':False,
        'cost_ring_slot':0
    }
}


def createSkillFromData(skillName,button):
    skillData=ALL_SKILL_DATA[skillName]
    name=skillData['name']
    effect=skillData['effect']
    dice_count=skillData['dice_count']
    dice_sides=skillData['dice_sides']
    fixed_damage=skillData['fixed_damage']
    hit_bonus=skillData['hit_bonus']
    is_ranged=skillData['is_ranged']
    range=skillData['range']
    cost_action=skillData['cost_action']
    cost_bonus=skillData['cost_bonus']
    cost_reaction=skillData['cost_reaction']
    cost_ring_slot=skillData['cost_ring_slot']
    return Skill(name,button,effect,dice_count,dice_sides,fixed_damage,hit_bonus,is_ranged,range,cost_action,cost_bonus,cost_reaction,cost_ring_slot)



HERO_DATA={
    '水月':{
        "name": "水月",
        "team": "hero",
        "occupation": "战士",
        "x": 200,
        "y": 200,
        "atk_range": 200,
        "act": 1,
        "level": 1,
        "strength": 13,
        "dexterity": 13,
        "intelligence": 15,
        "perception": 10,
        "constitution": 10,
        "charisma": 10,
        "skill_names": ["regular_attack"],
        "animation": {
            "char_folder": "mizuki_animations",
            "skin_folder": "mizuki_game_skin",
            "char_prefix": "mizuki",
            "frame_counts": {
                "attack": 43,
                "skill": 40,
                "idle": 260,
                "die": 30,
                "move": 40
            }
        }
    },

    '德克萨斯':{
        "name": "德克萨斯",
        "team": "hero",
        "occupation": "游荡者",
        "x": 200,
        "y": 600,
        "atk_range": 200,
        "act": 1,
        "level": 1,
        "strength": 12,
        "dexterity": 15,
        "intelligence": 13,
        "perception": 10,
        "constitution": 10,
        "charisma": 10,
        "skill_names": ["regular_attack"],
        "animation": {
            "char_folder": "texas_animations",
            "skin_folder": "texas_time_skin",
            "char_prefix": "texas",
            "frame_counts": {
                "attack": 28,
                "skill": 28,
                "idle": 80,
                "die": 30,
                "move": 40
            }
        }
    }
}


ENEMY_DATA={
    'sog':{
        "team": "enemy",
        "occupation": "游荡者",
        "atk_range": 200,
        "act": 1,
        "level": 1,
        "strength": 12,
        "dexterity": 15,
        "intelligence": 13,
        "perception": 10,
        "constitution": 10,
        "charisma": 10,
        "skill_names": ["regular_attack"],
        "animation": {
            "char_folder": "sog_animations",
            "skin_folder": "sog_re_skin",
            "char_prefix": "sog",
            "frame_counts": {
                "attack": 70,
                "move": 20,
                "idle": 30,
                "die": 30
            }
        }
    }
}

def createHero(app,heroName):
    heroData = HERO_DATA[heroName]
    name = heroData['name']
    team = heroData['team']
    occupation = heroData['occupation']
    x = heroData['x']
    y = heroData['y']
    atk_range = heroData['atk_range']
    act = heroData['act']
    level = heroData['level']
    strength = heroData['strength']
    dexterity = heroData['dexterity']
    intelligence = heroData['intelligence']
    perception = heroData['perception']
    constitution = heroData['constitution']
    charisma = heroData['charisma']
    skill_names = heroData['skill_names']
    animation = heroData['animation']
    skills=getSkillsList(skill_names)
    actions=load_char_actions(app,animation)
    hero=Unit(app,name, team, occupation, x, y, atk_range, act, level,strength, dexterity, intelligence, perception,constitution, charisma, actions, skills)
    hero.startTurn()
    return hero


def createEnemy(app,enemyName,name,x,y):
    enemyData = ENEMY_DATA[enemyName]
    team = enemyData['team']
    occupation = enemyData['occupation']
    atk_range = enemyData['atk_range']
    act = enemyData['act']
    level = enemyData['level']
    strength = enemyData['strength']
    dexterity = enemyData['dexterity']
    intelligence = enemyData['intelligence']
    perception = enemyData['perception']
    constitution = enemyData['constitution']
    charisma = enemyData['charisma']
    skill_names = enemyData['skill_names']
    animation = enemyData['animation']
    actions=load_char_actions(app,animation)
    skills=getSkillsList(skill_names)
    enemy=Unit(app,name, team, occupation, x, y, atk_range, act, level,strength, dexterity, intelligence, perception,constitution, charisma, actions, skills)
    enemy.startTurn()
    return enemy

def getSkillsList(skill_names):
    skills=[]
    for name in skill_names:
        button=Button(None,None,None,None,name)
        skill=createSkillFromData(name,button)
        skills.append(skill)
    return skills

