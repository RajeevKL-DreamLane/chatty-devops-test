# chatty-devops-test

## Description
deploy a django application on a vm with the following requirements

## Infra Setup
- [] share your public key with the hiring manager to get access to the VM.
- [] clone the project to the vm

#### part 1 - python and environment
- [] install python3.11 `make sure to install python3.11-full`
- [] install pipenv to setup virtual environment for the project `pipenv is pip package, do not install the linux package`
- [] install the required pip packages (refer the Pipfile)

#### part 2 - docker and mysql database
- [] setup docker with mysql
- [] create a database in mysql with name `chatty`, user `mysql` and password `chatty-password`

#### part 3 - django application
- [] to initialize the database, run the following command from the project directory
```pipenv run python manage.py migrate```
- [] to run the server, run the following command from the project directory
```pipenv run python manage.py runserver```
note: the server should be running on port 8000

#### part 4 - nginx
- [] setup nginx to serve the application on port 80
- [] to check if the application is running, visit the following url
```http://<ip-address>/admin```

### Bonus Points
- [] setup https with letsencrypt and serve the application on port 443
- [] setup gunicorn and serve the application using gunicorn
- [] setup supervisor to manage the gunicorn process
- [] implement setup automation using ansible


#### Note
    - you can use any automation tool to setup the infra like ansible, jenkins, etc. or you can do it manually.
    - you can use any guide or tutorial to setup the infra.
    - you can use any gpt tool to generate the commands.
