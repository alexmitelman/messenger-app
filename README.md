# Messenger App

## Intro

I decided to use WebSockets for instant messaging. Key features
- it maintains a full-duplex permanent connection between client and server
- memory and performance efficient on the server side
- supported by all modern browsers and is part of HTML5 standard

### Trade-offs

- This is more of a POC version, I prioritized speed of development overtests.
- Keeping code as clean as it gets, no excuses. PEP8 for Python, camelcase for JavaScript.
- Design was borrowed online. Let's pretend we have a web-designer in our team for this project. (Credit: Mutiullah Samim)

## Technologies

- Python + Django on the backend
- ```channels``` library for support WebSockets in Django (```channels``` is [officially](https://www.djangoproject.com/weblog/2016/sep/09/channels-adopted-official-django-project/) adopted by Django, however, it's being distributed separately)
- Redis for the channel layer (we don't use it directly)

## Install

Python and Docker should be installed on your machine.

### Redis

    docker pull redis
    docker run -p 6379:6379 -d redis
    
### Python
I was using Python 3.6.5 + Pipenv for virtual environment. 

    pipenv install
    pipenv shell

If you choose other virtual environment manager, you can install packages with:

    pip3 install -r requirements.txt

### Django

    cd backend/
    ./manage.py migrate
Create at least two or three users. To save time I decided to use Django's auth system for admins

    ./manage.py createsuperuser
    ...
    ./manage.py runserver

### Browser UI

Navigate to http://127.0.0.1:8000
Log in with one of the users we've created on the previous step. Navigate to the correspondence with another user by putting their name into the URL like this: http://127.0.0.1:8000/Billy/

	
## TODO and future improvements

1. Design API
2. Implement front-end on React.js (currently plain JavaScript)
	- single page app
	- mobile apps with React Native
3. Asyncronous server with ```async``` ``await`` for better backend performance
3. Adding more messenger features: online status, mark message as read, contact list etc.
4. Group chats. It would be easy to add them to the current architecture.

## Scalability

I would use Apache Cassandra as a database engine. This database system was initially designed by Facebook and would work incredibly fast for our purposes. It's has a linear scalability, can contain hundreds and thousand nodes in a cluster.

At the initial phase of the project, however, PostgreSQL would work well, we could use it as our database while working on the integration of Cassandra because t's not a RDBS system, and it would require changes in the code (models), as there is no foreign keys concept, for example. (Current implementation is on SQLite, let's assume it would be a quick switch to PostgreSQL.)

Putting WebSockets behind the load balancer is not straightforward but achievable