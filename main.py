from flask import Flask, render_template
import json

from utils import get_publics, get_nonces, get_chain_rpcs, get_stored_nonces

app = Flask(__name__)


@app.route("/")
def main():
    CHAIN_RPC = get_chain_rpcs("chain_rpcs.json")
    publics = get_publics("publics.txt")
    return render_template("index.html",
                           publics=publics,
                           nonces=get_stored_nonces(),
                           chains=CHAIN_RPC)


@app.route("/refresh")
def refresh_loading():
    return '''<h1>Loading</h1>
        <script> window.location.replace('refresh_done'); </script>
        '''


@app.route("/refresh_done")
def refresh_done():
    CHAIN_RPC = get_chain_rpcs("chain_rpcs.json")
    publics = get_publics("publics.txt")
    nonces = get_nonces(publics, CHAIN_RPC)
    with open("nonces.json", "w") as f:
        f.write(json.dumps(nonces))
    return "<h1>Refreshed !</h1>"
