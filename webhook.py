import main
import requests
import user
import json


def topLogin(data: list) -> None:
    endpoint = main.webhook_discord_url

    rewards: user.Rewards = data[0]
    login: user.Login = data[1]
    bonus: user.Bonus or str = data[2]
    
    with open('login.json', 'r', encoding='utf-8')as f:
        data22 = json.load(f)
        
        fpids1 = data22['cache']['replaced']['userGame'][0]['friendCode']
        Svtcount = sum(1 for item in data22['cache']['replaced']['userSvt'] if item.get('svtId') == 2300900) # 謎の代行者C.I.E.L
        Svtcount2 = sum(1 for item in data22['cache']['replaced']['userSvt'] if item.get('svtId') == 1001800) # カズラドロップ

    

    messageBonus = ''
    nl = '\n'

    if bonus != "No Bonus":
        messageBonus += f"__{bonus.message}__{nl}```{nl.join(bonus.items)}```"

        if bonus.bonus_name != None:
            messageBonus += f"{nl}__{bonus.bonus_name}__{nl}{bonus.bonus_detail}{nl}```{nl.join(bonus.bonus_camp_items)}```"

        messageBonus += "\n"

    jsonData = {
        "content": None,
        "embeds": [
            {
                "title": "FGO登录系统 - " + main.fate_region,
                "description": f"登录成功。列出角色信息.\n\n{messageBonus}",
                "color": 563455,
                "fields": [
                     {
                        "name": "ID", 
                        "value": f"{fpids1}",
                        "inline": True
                    }, 
                    {
                        "name": "呼符", 
                        "value": f"{rewards.ticket}",
                        "inline": True
                    },                    
                    {
                        "name": "圣晶石",
                        "value": f"{rewards.stone}",
                        "inline": True
                    },
                    {
                        "name": "AP",
                        "value": f"{login.remaining_ap}",
                        "inline": True
                    },
                    {
                        "name": "謎の代行者C.I.E.L",
                        "value": f"{Svtcount}",
                        "inline": True
                    },
                    {
                        "name": "カズラドロップ",
                        "value": f"{Svtcount2}",
                        "inline": True
                    },
                    
                ],
                "thumbnail": {
                    "url": "https://www.fate-go.jp/manga_fgo/images/commnet_chara01.png"
                }
            }
        ],
        "attachments": []
    }

    headers = {
        "Content-Type": "application/json"
    }

    requests.post(endpoint, json=jsonData, headers=headers)


def shop(item: str, quantity: str) -> None:
    endpoint = main.webhook_discord_url
    
    jsonData = {
        "content": None,
        "embeds": [
            {
                "title": "FGO自动购物系统 - " + main.fate_region,
                "description": f"购买成功.",
                "color": 5814783,
                "fields": [
                    {
                        "name": f"商店",
                        "value": f"消费 {40 * quantity}Ap 购买 {quantity}x {item}",
                        "inline": False
                    }
                ],
                "thumbnail": {
                    "url": "https://www.fate-go.jp/manga_fgo2/images/commnet_chara10.png"
                }
            }
        ],
        "attachments": []
    }

    headers = {
        "Content-Type": "application/json"
    }

    requests.post(endpoint, json=jsonData, headers=headers)


def drawFP(servants, missions) -> None:
    endpoint = main.webhook_discord_url

    message_mission = ""
    message_servant = ""

    if (len(servants) > 0):
        servants_atlas = requests.get(
            f"https://api.atlasacademy.io/export/JP/basic_svt.json").json()

        svt_dict = {svt["id"]: svt for svt in servants_atlas}

        for servant in servants:
            objectId = servant.objectId
            if objectId in svt_dict:
                svt = svt_dict[objectId]
                message_servant += f"`{svt['name']}` "
            else:
                continue

    if(len(missions) > 0):
        for mission in missions:
            message_mission += f"__{mission.message}__\n{mission.progressTo}/{mission.condition}\n"

    jsonData = {
        "content": None,
        "embeds": [
            {
                "title": "FGO自动抽卡系统 - " + main.fate_region,
                "description": f"完成当日免费友情抽卡。列出抽卡结果.\n\n{message_mission}",
                "color": 5750876,
                "fields": [
                    {
                        "name": "友情卡池",
                        "value": f"{message_servant}",
                        "inline": False
                    }
                ],
                "thumbnail": {
                    "url": "https://www.fate-go.jp/manga_fgo/images/commnet_chara02_rv.png"
                }
            }
        ],
        "attachments": []
    }

    headers = {
        "Content-Type": "application/json"
    }

    requests.post(endpoint, json=jsonData, headers=headers)
