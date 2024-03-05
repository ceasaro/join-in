# join-in

## Quick setup
1) create project dir: `mkdir join-in` and change to that dir: `cd join-in`
2) checkout/clone project `git checkout git@github.com:ceasaro/join-in.git` 
3) create a virtual env: `python3 -m venv ~/.venv`
4) active virtual env: `. ~/.virtualenvs/join_in/bin/activate`
5) install dependencies: `pip install -r setup/requirements-dev.txt`
6) create local settings: `cp app/join_in/settings/local_settings_example.py app/join_in/settings/local_settings.py`
7) create database (Postgres): `createdb join_in`
8) modify your local settings to connect to the correct database.

### run application
1) activate virtual env: `. ~/.virtualenvs/join_in/bin/activate`
2) change to app dir: `cd [YOUR_PROJECT_DIR]/join-in/app`
3) run migrations: `./manage.py migrate`
4) run server `./manage.py runserver`
