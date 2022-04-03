
# django social app

**Django** based social media web application

## Features

- user authentication
- editing user's profile
- creating and managing posts
- creating and managing comments
- liking posts
- following other users
- searching for books using [itbook.store api](api.itbook.store)
- saving books to user's bookshelf

## Installation

 1. Clone this repository and install project dependencies in a virtual enviroment by running
`pip install -r requirements.txt` from project's root directory.

-------
2. Create PostgreSQL database

---------
3. Create .env file and provide the following variables:

`SECRET_KEY`

PostgreSQL database fields:
```
DB_NAME
DB_USER
DB_PASSWORD
```

Google OAuth keys, needed only to authenticate with google account:
```
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET
```

-------

4. Run migrations: `python manage.py migrate`

-------
5. To start the local server use this command: `python manage.py runserver`

To use google authentication, run server using: `python manage.py runserver_plus --cert-file cert.crt`
Please note that appropriate google API configuration is also required for this functionality to work
