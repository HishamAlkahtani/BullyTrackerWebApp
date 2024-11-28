from flask import Flask
from flask_cors import CORS

app = Flask(__name__, static_url_path="")
CORS(app)

import bullytracker.webviews
import bullytracker.watchendpoints
import bullytracker.auth

# Application structrued as per:
# https://flask.palletsprojects.com/en/2.2.x/patterns/packages/
