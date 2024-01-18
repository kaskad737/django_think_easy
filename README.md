Status of Last Deployment:<br>
<img src="https://github.com/kaskad737/django_think_easy/actions/workflows/django.yml/badge.svg?branch=master">
<br>

# django_think_easy

## How to run project

1. "git clone" this project
2. Create ".env" file in the root folder of the project with the following content (insert your values):

    ```text
    - SECRET_KEY=django-secret-key
    - DB_NAME=postgres-django-project-db-name
    - DB_USER=postgres-user
    - DB_PASSWORD=postgres-django-project-db-password
    - DB_PORT=1234 (default 5432)
    - EXTERNAL_DB_PORT=5431 (port in case you already have one base running on the same port in your system)
    - EXTERNAL_REDIS_PORT=6379 (port in case you already have one base running on the same port in your system)
    ```

3. In the root folder of the project, run "bash run.sh"

## Views description

1. Each registered user has access only to his own list of restaurants and only to his list of created visits.
2. A registered user can only create/update visits to restaurants of which he is the owner/creator.
3. Each user has access only to his/her own restaurant details, the restaurant details contain links to the visits, if any, created by the user.
4. Each user only has access to their own visit details.
5. A user with admin rights has the right to view everything and change everything
6. Anonymous user has access only to registration, to the page with password return if he forgot it and to the login page.

## Documentation for api endpoints

When the project is launched

<http://127.0.0.1:8000/swagger/>

## Tests

Tests are run every time a commit is pushed to the repository. On the main page of this repo you can also see the result of testing workflow. Testing was realized through "Git Actions".
