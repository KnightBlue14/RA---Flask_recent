#!/usr/bin/env python3

from flask import Flask, render_template
import os
from flask_apscheduler import APScheduler
import ret_auth
import json
import requests
import ret_auth
import shutil

app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True

key = 'Jcu6C3oyn4WdBEeYnD1bFXHiVqytKe2s'
user = 'KnightBlue'


def refresh():
    url_recent = f'https://retroachievements.org/API/API_GetUserRecentAchievements.php?u={user}&y={key}'
    response = requests.post(url_recent)

    folder_name = "static\\images"

    try:
        with open('./cache.json') as d:
            f = json.load(d)
    except FileNotFoundError:
        f = 'no cache found'

    if len(response.json()) == 0 and len(f) == 1:
        data = f
    elif response.json() == f:
        data = f
    else:
        try:
            os.remove("./static\\images\\cover.png")
            os.remove("./static\\images\\badge.png")
        except FileNotFoundError:
            pass 
        with open("./cache.json", "wb") as f:
            f.write(response.content)
        data = response.json()

    game_url = data[0]['GameIcon']
    cover_response = requests.get(f'https://i.retroachievements.org/{game_url}', stream=True)
    cover = open(f"{folder_name}\\cover.png",'wb')
    shutil.copyfileobj(cover_response.raw, cover)
    cover.close()

    ach_url = data[0]['BadgeURL']
    ach_response = requests.get(f'https://i.retroachievements.org/{ach_url}', stream=True)
    ach = open(f"{folder_name}\\badge.png",'wb')
    shutil.copyfileobj(ach_response.raw, ach)
    ach.close()

def ach_name():
    try:
        data = json.load(open('cache.json'))
        game_title = data[0]['GameTitle']
        ach_title = data[0]['Title']
        ach_desc = data[0]['Description']
        return [game_title,ach_title,ach_desc]
    except Exception:
        return ['Cache file not found','Please make sure that you have unlocked an achievement within the last hour','and that your api key is valid']

@app.route("/")
def home():
    cover_url = "static\\images\\cover.png"
    badge_url = "static\\images\\badge.png"
    return render_template('index.html',image_url=cover_url,
                           badge_url = badge_url,
                           game_title = ach_name()[0],
                           ach_title = ach_name()[1],
                           ach_desc = ach_name()[2])



scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
scheduler.add_job(id='refresh', func=refresh, trigger='interval', seconds=10)


if __name__ == '__main__':
    app.run()
