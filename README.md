# BullyTrackerWebApp

Repo for the web app part of bully tracker

## Build Intsructions

To run the app on your machine, you must have python, pip, and git installed. You must also have the cred.json file. Run the following in the terminal:

```shell
git clone "https://github.com/HishamAlkahtani/BullyTrackerWebApp"
cd BullyTrackerWebApp
pip install -e .
flask --app bullytracker run --debug
```

## TODO

### Front End
- [X] Link login/register pages to firebase authentication
- [ ] Client side form validation on all forms
- [ ] Make the school name field in the parent registration form a drop down menu that shows available schools
- [ ] Remove the username field from the register page, as it is useless. A full name field will be more useful.
- [ ] Proper error messages when register fails
- [ ] Geofencing: Figure out how the map UI will work
- [ ] Parent dashboard
- [ ] Whatsapp list page: the page that allows the school admin to add/remove numbers from the messaging list that will recieve the alerts
- [X] Watch Setup Page Prototype 
- Should the entire watch setup page be refreshed every time period to update the watch statuses or 
### Back End
- [X] Display different home page based on type of user that's logged in; If a school admin is logged in, they should see the dashboard of their school. If the logged in user is a parent, they should see their children's info
- [ ] Proper error message when register fails
- [X] Make the user class fetch all relevant properties from firstore upon creation
- [X] Admin ability to remove watch
- [ ] Endpoints to serve real time updates to frontend (like student locations, pending alerts, etc...)
- [ ] BUG: When alerts are stored in firestore, the timestamp is off by three hours, this could be because of an issue with how the python date object is handled by the firestore package
- [X] Whatsapp messaging: school admin able to add/remove contacts
- [X] Create school whatsapp messaging list
- [X] SOS Alerts are sent to everyone in the school's whatsapp messaging list
#### Caching and performance
- Cache layer vs in-memory data + some synch mechanism? will it be needed at all? or will the performance of just firestore be enough? what tasks can be cached? Look into flask_caching and redis
- should active_alerts be cached?
#### Geofencing
- [X] Figure out a way to determine if a student's coordinate are within a certain location
- [ ] Enable the school admin to add boundaries
#### Watch App API
- [X] Setup process (tentative):
    - [X] 1) Setup an endpoint for the watch app to call, it randomly generates a string id and checks firestore to see if the generated id already exists
    - [X] 2) Setup an endpoint for the watch app to call periodically to check if the watch has been activated or not
    - [X] 3) When the school admin chooses the watch and enters the displayed watch id in the app, the endpoint tells the watch that the watch is currently being linked, and tells the watch the name of the school that is trying to connect to it...
    - [X] 4) On the display of the watch, a prompt is shown, if YES is clicked on the watch, the setup process is now complete, and the watch is now active.
- [X] Store received alerts from watch in DB
- [ ] Alert handling (after an alert is addressed, the alert is moved to the previousAlerts collection, and a report can be attached to the alert)
- [ ] An endpoint to receive periodic updates from the watch (and where should they be stored?)
### Firebase
- [X] Geofencing: Figure out how the coordinates should be stored.
