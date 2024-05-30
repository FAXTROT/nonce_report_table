from functools import wraps

from flask import Flask, render_template, flash, redirect, session, url_for, request
import json

import hashlib

from utils import get_publics, get_nonces, get_chain_rpcs, get_stored_nonces

app = Flask(__name__)
app.secret_key = "a1f528f25901cb6b3942c0101eeaf7e534a64af8c11d58564971c8d139e356ac"


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        psw_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

        # Dummy user validation
        if username == 'uname1' and psw_hash == 'a1f528f25901cb6b3942c0101eeaf7e534a64af8c11d58564971c8d139e356ac':
            session['username'] = username
            session['psw_hash'] = psw_hash
            return redirect(url_for('home'))
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('psw_hash', None)
    return redirect(url_for('login'))


def login_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        try:
            username = session['username']
            psw_hash = session['psw_hash']
            if username == 'uname1' and psw_hash == 'a1f528f25901cb6b3942c0101eeaf7e534a64af8c11d58564971c8d139e356ac':
                session['username'] = username
                session['psw_hash'] = psw_hash
                return f(*args, **kwargs)
            else:
                return render_template('login.html')
        except Exception as err:
            return render_template('login.html')
    return decorator
###


@app.route("/home")
@login_required
def home():
    return render_template("welcome.html")


@app.route("/")
@login_required
def main():
    CHAIN_RPC = get_chain_rpcs("chain_rpcs.json")
    publics = get_publics("publics.txt")
    return render_template("index.html",
                           publics=publics,
                           nonces=get_stored_nonces(),
                           chains=CHAIN_RPC)


@app.route("/refresh")
@login_required
def refresh_loading():
    return '''<h1>Loading</h1>
        <script> window.location.replace('refresh_done'); </script>
        '''


@app.route("/refresh_done")
@login_required
def refresh_done():
    CHAIN_RPC = get_chain_rpcs("chain_rpcs.json")
    publics = get_publics("publics.txt")
    nonces = get_nonces(publics, CHAIN_RPC)
    with open("nonces.json", "w") as f:
        f.write(json.dumps(nonces))
    return redirect(url_for('main'))


@app.route("/edit/publics", methods=['GET'])
@login_required
def edit_publics_get():
    publics = get_publics("publics.txt")
    return render_template("edit/edit_publics.html", publics=publics)


@app.route("/edit/publics", methods=['POST'])
@login_required
def edit_publics_post():
    publics = request.form['publics']
    with open("publics.txt", "w") as f:
        f.write(publics)
    return redirect(url_for('refresh_loading'))


@app.route("/edit/configs", methods=['GET'])
@login_required
def edit_configs_get():
    with open("chain_rpcs.json", "r") as f:
        configs = f.read()
    return render_template("edit/edit_configs.html", configs=configs)


@app.route("/edit/configs", methods=['POST'])
@login_required
def edit_configs_post():
    configs = request.form['configs']
    with open("chain_rpcs.json", "w") as f:
        f.write(configs)
    return redirect(url_for('refresh_loading'))
