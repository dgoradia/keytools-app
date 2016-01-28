# Title:            SSH Key Tools
# Description:      Simple REST Api for working with SSH
# Author:           Dru Goradia
# Date:             01/26/2016
# Version:          1.0.0
# Python Version:   2.6.6
from flask import Flask, url_for, request, json, jsonify
from flask.ext.cors import CORS
from Crypto.PublicKey import RSA
import logging
file_handler = logging.FileHandler('app.log')

app = Flask(__name__)
CORS(app)

app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

@app.route('/')
def api_root():
    return "Key Tools service running...\n"

@app.route('/key2pub', methods = ['POST'])
def api_keypub():
    # if request.headers['Content-Type'] == 'application/json; charset=UTF-8':
    resp = None

    if request.json['key'] == '':
        resp = jsonify({"error": "Please provide an RSA key"})
        resp.status_code = 422
        return resp

    try:
        pubkey = RSA.importKey(request.json['key'], request.json['passphrase']).exportKey('OpenSSH')
        resp = jsonify({"public_key": pubkey})
    except ValueError as e:
        if str(e) == 'RSA key format is not supported':
            resp = jsonify({"error": "Incorrect key or passphrase", "raw": str(e)})
            resp.status_code = 401
        elif str(e) == 'PEM encryption format not supported.':
            resp = jsonify({"error": "Passphrase protected", "raw": str(e)})
            resp.status_code = 422
        else:
            resp = jsonify({"error": "Unexpected error", "raw": str(e)})

    return resp
    # else:
    #     resp = jsonify()
    #     resp.status_code = 418
    #     return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4999, debug=False);
