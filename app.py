from flask import (Flask, 
                  render_template,
                  request,
                  session,
                  redirect,
                  g,
                  abort,
                  flash,
                  url_for)

import os

def get_root_dir():
    root_path = os.path.abspath('.')
    return root_path


class AudioPlayer:
    def __init__(self):
        wsl = os.environ.get('WSL',None)
        self._wsl = False
        if wsl is not None and wsl.lower() == 'true':
            print('WSL Enabled')
            self._wsl = True
    def play(self, song):
        if self._wsl:
            print(f'playing {song}')
    def stop(self):
        if self._wsl:
            print(f'stop song')

#app = Flask(__name__)
def create_app():
    app = Flask(__name__)

    with app.app_context():
        if 'audio_player' not in g:
            g.audio_player = AudioPlayer()

    app.secret_key = 'somelongsecretkey'
    
    return app

app = create_app()

class User:
    def __init__(self,id,username,password):
        self.id = id
        self.username = username
        self.password = password

users = [User(1,'sean','hello')]

class Button:
    def __init__(self, name):
        self._name = name
        self._on = False
        self._all_classes = {False:"sndBtn",True:"sndBtnOn"}
        self._class = self._all_classes[False]
        self._file = None

    def get_on(self):
        return self._on
    
    def set_on(self, on):
        self._on = on
        self._class = self._all_classes[self._on]

    def set_file(self, file):
        self._file = file

    def get_file(self):
        return self._file

    def toggle(self):
        self._on = not self._on
        self._class = self._all_classes[self._on]

buttons = [Button(i) for i in range(8)]

@app.before_request
def before_request():
    g.user = None
    g.buttons = buttons
    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user
        g.root_path = get_root_dir()


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        print('Post success')
        session.pop('user_id',None)
        username = request.form['username']
        password = request.form['password']

        user = [x for x in users if x.username == username ]
        if len(user) == 0:
            user = None
        else:
            user = user[0]
        if user and user.password == password:
            session['user_id'] = user.id
            print('Success')
            return redirect(url_for('profile'))
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/profile', methods=["GET","POST"])
def profile():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('profile.html')


@app.route("/sound-button", methods=["GET","POST"])
def sound_button():

    print(f"request.form: {request.form}")

    if request.method == "GET":
        return render_template('profile.html')

    print("sound_button")
    print(f"request.form: {request.form.keys()}")
    if request.method  == "POST":
        for i,b in enumerate(buttons):
            if f"{i}" in request.form:
                buttons[i].toggle()
                flash(f"Play [{i}]: {buttons[i].get_file()}")
            else:
                buttons[i].set_on(False)

        #if len(request.form.keys()) > 0:
        #    pressed = list(request.form.keys())
        #    g.status = f'Now Playing: {pressed}'

    return render_template('profile.html')

@app.route("/load-config",methods=["POST"])
def load_config():
    import json
    with open('config.json','r') as fp:
        config = json.load(fp)

    for i,k in config.items():
        index = int(i)
        buttons[index].set_file(k)
        buttons[index].set_on(False)

    flash('config.json loaded.')
    return render_template('profile.html')

@app.route("/save-config",methods=["POST"])
def save_config():
    config = {i:k.get_file() for i,k in enumerate(buttons)}
    import json
    with open('config.json','w') as fp:
        json.dump(config,fp)
    print('Saved config to config.json')
    flash('config.json saved.')
    return render_template('profile.html')

 
@app.route("/upload-sound", methods=["GET","POST"])
def upload_sound():
    # https://www.youtube.com/watch?v=6WruncSoCdI
    if request.method == "POST":
        if request.files:
            sound  = request.files["sound"]
            path = os.path.join(g.root_path,'static',sound.filename)

            for i,b in enumerate(buttons):
                if b._on:
                    print(f"Saving {path} to button {i}")
                    flash(f"Set Button [{i}]: {sound.filename}")
                    b.set_file(sound.filename)
                    sound.save(path)
                    break
            return redirect(request.url)
    return render_template('profile.html')

# run notes:
# export FLASK_ENV=developement
# flask run

# from https://www.youtube.com/watch?v=2Zz97NVbH0U


