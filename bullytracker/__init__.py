from flask import Flask

app = Flask(__name__)

import bullytracker.webviews
import bullytracker.watchendpoints

# Application structrued as per:
# https://flask.palletsprojects.com/en/2.2.x/patterns/packages/
