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


### Endpoint Usage

#### Submit Happiness Level Endpoint

`Authorization Required`

Endpoint
```
POST /happiness/submit/  
JSON {
    "rating": [1 - 10] (By default, range is changable in hb/settings.py)    
}
```

Response
```
JSON {
    "success": true,
    "id": <id_of_log>,
    "team_member": <tm_id>,
    "rating": <rating>
}
```


Description

An authenticated user may **POST** to the above endpoint and register 
their happiness rating for the day.  If there is an already existing happiness 
rating it will trigger an error.  If the rating is outside the bounds, it 
will throw an error.

Will return details about the HappinessLevel recorded.


#### Team Stats Endpoint

`Authorization Optional`

Endpoint

```
GET /team/stats/
```

Response

The Response will differ if the user is authenticated.

Authenticated User Response

```
{
    "<Team Name>": {
        "average": <average>,
        "member_count_by_level": {
            "null": 1,
            "6": 3,
            "7": 2,
        }
    }
}
```

Please note, a `null` value in `member_count_by_level` indicates how many team
members have never registered their happiness levels.

Unauthenticated User Response

```
{
    "all_teams_average": <average>
}
```

Will fetch an average across all teams.
