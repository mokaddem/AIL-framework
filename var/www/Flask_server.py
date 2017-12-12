#!/usr/bin/env python2
# -*-coding:UTF-8 -*

import redis
import ConfigParser
import json
import datetime
import time
import calendar
from flask import Flask, render_template, jsonify, request
import flask
import importlib
import os
from os.path import join
import sys
sys.path.append(os.path.join(os.environ['AIL_BIN'], 'packages/'))
sys.path.append(os.path.join(os.environ['AIL_FLASK'], 'modules/'))
import Paste
from Date import Date

# Import config
import Flask_config

# CONFIG #
cfg = Flask_config.cfg

Flask_config.app = Flask(__name__, static_url_path='/static/')
app = Flask_config.app

# ========= HEADER GENERATION ========

# Get headers items that should be ignored (not displayed)
toIgnoreModule = set()
try:
    with open(os.path.join(os.environ['AIL_FLASK'], 'templates/ignored_modules.txt'), 'r') as f:
        lines = f.read().splitlines()
        for line in lines:
            toIgnoreModule.add(line)

except IOError:
    f = open(os.path.join(os.environ['AIL_FLASK'], 'templates/ignored_modules.txt'), 'w')
    f.close()


# Dynamically import routes and functions from modules
# Also, prepare header.html
to_add_to_header_dico = {}
for root, dirs, files in os.walk(os.path.join(os.environ['AIL_FLASK'], 'modules/')):
    sys.path.append(join(root))

    # Ignore the module
    curr_dir = root.split('/')[1]
    if curr_dir in toIgnoreModule:
        continue

    for name in files:
        module_name = root.split('/')[-2]
        if name.startswith('Flask_') and name.endswith('.py'):
            if name == 'Flask_config.py':
                continue
            name = name.strip('.py')
            #print('importing {}'.format(name))
            importlib.import_module(name)
        elif name == 'header_{}.html'.format(module_name):
            with open(join(root, name), 'r') as f:
                to_add_to_header_dico[module_name] = f.read()

#create header.html
complete_header = ""
with open(os.path.join(os.environ['AIL_FLASK'], 'templates/header_base.html'), 'r') as f:
    complete_header = f.read()
modified_header = complete_header

#Add the header in the supplied order
for module_name, txt in to_add_to_header_dico.items():
    to_replace = '<!--{}-->'.format(module_name)
    if to_replace in complete_header:
        modified_header = modified_header.replace(to_replace, txt)
        del to_add_to_header_dico[module_name]

#Add the header for no-supplied order
to_add_to_header = []
for module_name, txt in to_add_to_header_dico.items():
    to_add_to_header.append(txt)

modified_header = modified_header.replace('<!--insert here-->', '\n'.join(to_add_to_header))

#Write the header.html file
with open(os.path.join(os.environ['AIL_FLASK'], 'templates/header.html'), 'w') as f:
    f.write(modified_header)


# ========= JINJA2 FUNCTIONS ========
def list_len(s):
    return len(s)
app.jinja_env.filters['list_len'] = list_len


# ========= CACHE CONTROL ========
@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

# ========== ROUTES ============
@app.route('/searchbox/')
def searchbox():
    return render_template("searchbox.html")


# ============ MAIN ============

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7000, threaded=True)
