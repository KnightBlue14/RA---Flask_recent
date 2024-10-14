import requests
import ret_auth
from datetime import datetime
import shutil
import json
import os

user = ret_auth.user
key = ret_auth.key

url_recent = f'https://retroachievements.org/API/API_GetUserRecentAchievements.php?u={user}&y={key}'
response = requests.post(url_recent)

folder_name = 'static\\images'

try:
    with open('cache.json') as d:
        f = json.load(d)
except FileNotFoundError:
    f = 'no cache found'

if len(response.json()) == 0 and len(f) == 1:
    data = f
elif response.json() == f:
    data = f
else:
    try:
        os.remove('static\\images\\cover.png')
        os.remove('static\\images\\badge.png')
    except FileNotFoundError:
        pass 
    with open("cache.json", "wb") as f:
        f.write(response.content)
    data = response.json()
    game_cover = data[0]['GameIcon']
    cover_response = requests.get(f'https://i.retroachievements.org/{game_cover}', stream=True)
    cover_path = 'static\\images\\cover.png'
    cover = open(f'{folder_name}\\cover.png','wb')
    shutil.copyfileobj(cover_response.raw, cover)
    cover.close()
    ach_url = data[0]['BadgeURL']
    ach_response = requests.get(f'https://i.retroachievements.org/{ach_url}', stream=True)
    badge_path = 'static\\images\\badge.png'
    ach = open(f'{folder_name}\\badge.png','wb')
    shutil.copyfileobj(ach_response.raw, ach)
    ach.close()
    
game_title = data[0]['GameTitle']

ach_title = data[0]['Title']
ach_desc = data[0]['Description']
