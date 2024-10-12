from flask import Flask

app = Flask(__name__, static_url_path="")

import bullytracker.webviews
import bullytracker.watchendpoints
import bullytracker.auth

# Application structrued as per:
# https://flask.palletsprojects.com/en/2.2.x/patterns/packages/
