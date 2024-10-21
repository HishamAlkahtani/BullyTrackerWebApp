# BullyTrackerWebApp

Repo for the web app part of bully tracker

## Build Intsructions

To run the app on your machine, you must have python, pip, and git installed. Run the following in the terminal:

```shell
git clone "https://github.com/HishamAlkahtani/BullyTrackerWebApp"
cd BullyTrackerWebApp
pip install -e .
flask --app bullytracker run --debug
```

## TODO

### Front End
- [X] Link login/register pages to firebase authentication
- [ ] Form validation on register and login form
- [ ] Make the school name field in the parent registration form a drop down menu that shows available schools
- [ ] Proper error messages when register fails
- [ ] Geofencing: Figure out how the map UI will work
- [ ] Parent dashboard
- [ ] Whatsapp list page: the page that allows the school admin to add/remove numbers from the messaging list that will recieve the alerts
- [ ] Watch Setup Page
### Back End
- [ ] Geofencing: Figure out a way to determine if a student's coordinate are within a certain location
- [ ] Display different home page based on type of user that's logged in; If a school admin is logged in, they should see the dashboard of their school. If the logged in user is a parent, they should see their children's info
- [ ] Watch Setup Process
- [ ] Proper error message when register fails
### Firebase
- [ ] Geofencing: Figure out how the coordinates should be stored.
