
# django social app

**Django** based social media web application that also utilizes Google's and other external APIs

## Features

- user authentication
- editing user's profile
- creating and managing posts
- creating and managing comments
- liking posts
- following other users
- searching for books using [itbook.store api](https://api.itbook.store)
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

## Screenshots
![homepage](https://user-images.githubusercontent.com/68167747/161774289-7c009fce-9aca-4da3-80b7-84caed751faa.jpg)
![myact](https://user-images.githubusercontent.com/68167747/161775317-6671fb68-2282-4237-8ff9-a1a45e87fb5f.jpg)
![mybooks](https://user-images.githubusercontent.com/68167747/161775339-3ebed6a5-b7f0-41c4-868a-eae4b389879a.jpg)



