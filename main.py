from flask import Flask, render_template

from config import DELAY_RPC_CALLS, CHAIN_RPC

from utils import get_publics, get_nonces

app = Flask(__name__)


@app.route("/")
def main():
    publics = get_publics("publics.txt")
    return render_template("index.html",
                           publics=publics,
                           nonces=get_nonces(publics, CHAIN_RPC),
                           chains=CHAIN_RPC)
