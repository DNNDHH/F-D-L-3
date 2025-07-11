import os
import requests
import time
import json
import fgourl
import user
import coloredlogs
import logging

# Enviroments Variables
userIds = os.environ['userIds'].split(',')
authKeys = os.environ['authKeys'].split(',')
secretKeys = os.environ['secretKeys'].split(',')
webhook_discord_url = os.environ['webhookDiscord']
device_info = os.environ.get('DEVICE_INFO_SECRET')
appCheck = os.environ.get('APP_CHECK_SECRET')
user_agent_2 = os.environ.get('USER_AGENT_SECRET_2')
fate_region = 'JP'

userNums = len(userIds)
authKeyNums = len(authKeys)
secretKeyNums = len(secretKeys)

logger = logging.getLogger("FGO")
coloredlogs.install(fmt='%(asctime)s %(name)s %(levelname)s %(message)s')

def get_latest_verCode():
    endpoint = "https://raw.githubusercontent.com/DNNDHH/FGO-VerCode-extractor/JP/VerCode.json"
    response = requests.get(endpoint).text
    response_data = json.loads(response)

    return response_data['verCode']
    
def get_latest_appver():
    endpoint = "https://raw.githubusercontent.com/DNNDHH/FGO-VerCode-extractor/JP/VerCode.json"
    response = requests.get(endpoint).text
    response_data = json.loads(response)

    return response_data['appVer']

def main():
    if userNums == authKeyNums and userNums == secretKeyNums:
        fgourl.set_latest_assets()

        for i in range(userNums):
            try:
                instance = user.user(userIds[i], authKeys[i], secretKeys[i])
                time.sleep(1)
                logger.info('登录账号!')
                instance.topLogin()
                time.sleep(1)
                instance.topHome()
                time.sleep(0.5)
                instance.buyBlueApple()
                instance.lq001()
                time.sleep(0.5)
                instance.Present()
                time.sleep(0.5)
                instance.lq002()
                time.sleep(1)
                instance.lq003()
                time.sleep(1)
                #instance.buyitem_myseif()
                time.sleep(1)
                instance.zc15()
                
                #instance.zc16()
                #instance.zc25() #导出账号功能
                
                instance.drawFPT1S()
                #for _ in range(100): 
                      #instance.drawS()
                      #instance.drawFF()
                      #time.sleep(1)
                    
            except Exception as ex:
                logger.error(ex)


if __name__ == "__main__":
    main()
