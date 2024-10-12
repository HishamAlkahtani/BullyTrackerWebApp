# Contains all the endpoints that the watch will make requests to

from bullytracker import app

alerts = []
numOfWatches = 0


# The app recieves alerts from the watch on this endpoint
@app.route("/alert/<name>/<location>")
def recvAlert(name, location):
    msg = "Alert Recieved from: " + name + " At location: " + location
    alerts.append(msg)
    print(msg)
    return "Alert recieved"


@app.route("/getWatchId")
def assignWatchId():
    # NOT THREAD SAFE!
    # TODO: figure out to store data in-memory
    global numOfWatches
    numOfWatches = numOfWatches + 1
    return str(numOfWatches)
