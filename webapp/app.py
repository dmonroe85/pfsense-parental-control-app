import os, sys, json
from flask import Flask, jsonify, send_file
from flask_cors import CORS
from PfsenseFauxapi.PfsenseFauxapi import PfsenseFauxapi

app = Flask(__name__)

CORS(app)

_, conf_file = sys.argv

with open(conf_file, 'r') as infile:
    conf = json.load(infile)

PFSENSE_HOST = conf['PFSENSE_HOST']
apikey = conf['FAUXAPI_APIKEY']
apisecret = conf['FAUXAPI_APISECRET']

api = PfsenseFauxapi(PFSENSE_HOST, apikey, apisecret)
api.proto = 'http'

# Serving the web site
@app.route('/')
def index():
    return send_file(os.path.join('build', 'index.html'))

@app.route('/<path:path>')
def root_files(path):
  # send_static_file will guess the correct MIME type
  return send_file(os.path.join('build', path))

@app.route('/static/css/<path:path>')
def css_files(path):
  # send_static_file will guess the correct MIME type
  return send_file(os.path.join('build', 'static', 'css', path))

@app.route('/static/js/<path:path>')
def js_files(path):
  # send_static_file will guess the correct MIME type
  return send_file(os.path.join('build', 'static', 'js', path))

# Blocklist API
@app.route('/get_blocked', methods=['GET'])
def get_config():
    config = api.config_get()
    rules = config['filter']['rule']
    return jsonify(sorted(set([r['descr'].split(':')[0] for r in rules if not r['descr'].startswith('Default')])))


if __name__ == '__main__':
    app.run(host='0.0.0.0')