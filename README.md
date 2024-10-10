# chatty-devops-test

## Description
this is a test repo for testing devops setup

## Infra Setup
- [x] share your public key with the hiring manager to get access to the VM.

- [x] clone the project to the vm
- [x] install the required version of python (refer the Pipfile)
- [x] install pipenv to setup virtual environment for the project
- [x] install the required packages (refer the Pipfile)

- [x] setup docker with mysql
- [x] create a database in mysql with name `chatty`, user `mysql` and password `chatty-password`

- [x] to initialize the database, run the following command from the project directory
```pipenv run python manage.py migrate```
- [x] to run the server, run the following command from the project directory
```pipenv run python manage.py runserver```
note: the server should be running on port 8000

- [x] setup nginx to serve the application on port 80
- [x] to check if the application is running, visit the following url
```http://<ip-address>/admin```

### Bonus Points
- [x] setup https with letsencrypt and serve the application on port 443
- [x] setup gunicorn and serve the application using gunicorn
- [x] setup supervisor to manage the gunicorn process
- [x] implement setup automation using ansible
