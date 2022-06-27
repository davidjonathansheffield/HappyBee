# HappyBee
#### "Bee Happy!"
### Happiness Management Software for Teams

## Installation

1. Clone this repo into your project directory
2. Create a virtual environment using `Python 3.9`
3. Run `pip install -r requirements.txt`
4. Run `python3 manage.py runserver 8000`
5. Access on `localhost:8000`

## Documentation

### Creating First User
1. Run `python3 manage.py createsuperuser`
2. Access the admin panel at `/admin/`

### User and Team Instantiation
1. From the admin panel, select `Teams` or goto `/admin/hb_app/team/`
2. Click `Add Team`.
3. Select a name for the team, and add as many users to the team as desired.

### Authorization
Authorization is done through **bearer tokens**.

#### Token Acquisition

Tokens can be acquired using the following endpoint:

```
POST /api-token-auth/ 
JSON {
    "username": "<username>",
    "password": "<password>",
}
```

Which will, upon success, return the following:

```
JSON {
    "token": "<token>",
}
```

### Token in Authorization Header

For the views below that require authorization, you must include the 
token you receive from the above mentioned endpoint in your Authorization
header with each request. 

Example using curl:

```
curl -X GET http://localhost:8000/happiness/submit/ -H 'Authorization: Token <token>'
```

### Timezone Settings
By default, the application is set to run in **UTC** time, this setting can be 
changed in `hb/settings.py`.  You may want to change this to your local
time as it determines what time constitutes a day to determine happiness
recordings.

