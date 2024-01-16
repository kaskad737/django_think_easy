Status of Last Deployment:<br>
<img src="https://github.com/kaskad737/django_think_easy/actions/workflows/django.yml/badge.svg?branch=master">
<br>

# django_think_easy

## Task assignment
Aim of this task is to create 'restaurant visit diary'. Our users like travel and they would like to write down their own reviews restaurants they have visited to know where to go next / to whom to recommend. It is therefore necessary to record the Restaurant and the Visit. At the Restaurant it is necessary to know the name, place, type (type of cuisine). The visit should records the date of the visit, the expense, a note (where the user can write down what he / she has given and other findings) and an evaluation (values ​​ranging from 1 to 5).
The system should use DB (we use Postgresql), but the default SQLite will suffice. The project should contain a README, which will include steps on how to run the project. The system should use Django and djangorestframework packages.
## Requirements
### project launch (docker):
- set Docker (or docker-compose) to run. I.e. create `Dockerfile` (and possibly` docker-compose.yml`) (django + ideally Postgresql)
- Create a shell script for easy execution.
- bonus: set django + docker for local startup and production startup (with env variables)
### django rest framework
- user registration and login via API (use [JWT] to log in (https://github.com/davesque/django-rest-framework-simplejwt))
- Ability to list, create, edit, delete restaurants.
- Possibility to create a Visit to a certain Restaurant (A visit to the Restaurant can be created only by the user who created the given Restaurant)
- Show all visits (date) and average rating and spending of all visits in the restaurant listing and dateil.
- bonus_1: Documentation for api endpoints should be available (we use [drf_yasg] (https://github.com/axnsan12/drf-yasg) to automatically generate documentation).
- bonus_2: sending an email when forgetting the password to the email (just write the email to the console, see [django docs] (https://docs.djangoproject.com/en/2.2/topics/email/#console-backend)) using queue ( eg [Celery] (https://docs.celeryproject.org/en/latest/django/first-steps-with-django.html))
- bonus_3 connection to 3rd party API (eg Zomato, which could list restaurants in a location)
## testing
- suggest a way to run tests.
- use buildin django unittest module and / or pousks
- bonus_1: use fixtures in testing
