from flask import Flask, render_template
import os
from flask_apscheduler import APScheduler
import ret_auth
import json

app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True

user = ret_auth.user
key = ret_auth.key


def refresh():
    os.system('tasks.py')
def ach_name():
    try:
        data = json.load(open('cache.json'))
        game_title = data[0]['GameTitle']
        ach_title = data[0]['Title']
        ach_desc = data[0]['Description']
        return [game_title,ach_title,ach_desc]
    except Exception:
        return ['Cache file not found','Please make sure that you have unlocked an achievement within the last hour','and that your api key is valid']

@app.route('/')
def home():
    cover_url = 'static\\images\\cover.png'
    badge_url = 'static\\images\\badge.png'
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
