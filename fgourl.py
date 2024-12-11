import json
import binascii
import requests
import main
import CatAndMouseGame

requests.urllib3.disable_warnings()
session = requests.Session()
session.verify = False

# ===== Game's parameters =====
app_ver_ = ''
data_ver_ = 0
date_ver_ = 0
ver_code_ = ''
asset_bundle_folder_ = ''
data_server_folder_crc_ = 0
server_addr_ = 'https://game.fate-go.jp'
github_token_ = ''
github_name_ = ''


# ==== User Info ====
def set_latest_assets():
    global app_ver_, data_ver_, date_ver_, asset_bundle_folder_, data_server_folder_crc_, ver_code_, server_addr_

    # Get Latest Version of the data!
    version_str = main.get_latest_appver()
    response = requests.get(
        'https://game.fate-go.jp/gamedata/top?appVer=' + version_str).text
    response_data = json.loads(response)["response"][0]["success"]

    # Set AppVer, DataVer, DateVer
    app_ver_ = version_str
    data_ver_ = response_data['dataVer']
    date_ver_ = response_data['dateVer']
    ver_code_ = main.get_latest_verCode()

    # Use Asset Bundle Extractor to get Folder Name
    assetbundle = CatAndMouseGame.getAssetBundle(response_data['assetbundle'])
    get_folder_data(assetbundle)


def get_folder_data(assetbundle):
    global asset_bundle_folder_, data_server_folder_crc_

    asset_bundle_folder_ = assetbundle['folderName']
    data_server_folder_crc_ = binascii.crc32(
        assetbundle['folderName'].encode('utf8'))

# ===== End =====
user_agent_2 = os.environ.get('USER_AGENT_SECRET_2')

httpheader = {
    'Accept-Encoding': 'deflate, gzip',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': user_agent_2,
    'X-Unity-Version': "2022.3.28f1"
}


def NewSession():
    return requests.Session()


def PostReq(s, url, data):
    res = s.post(url, data=data, headers=httpheader, verify=False).json()
    res_code = res['response'][0]['resCode']

    if res_code != '00':
        detail = res['response'][0]['fail']['detail']
        message = f'[ErrorCode: {res_code}]\n{detail}'
        raise Exception(message)

    return res
