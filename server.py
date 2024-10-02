from flask import Flask, render_template
import tasks
from livereload import Server
import os
from flask_apscheduler import APScheduler

app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True

def refresh():
    os.system('tasks.py')

@app.route('/')
def home():
    cover_url = 'static\\images\\cover.png'
    badge_url = 'static\\images\\badge.png'
    return render_template('index.html',image_url=cover_url,
                           badge_url = badge_url,
                           game_title = tasks.game_title,
                           ach_title = tasks.ach_title,
                           ach_desc = tasks.ach_desc)



scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
scheduler.add_job(id='refresh', func=refresh, trigger='interval', seconds=1)


if __name__ == '__main__':
    app.run()


# if __name__ == '__main__':
#     server = Server(app.wsgi_app)
#     server.serve()
