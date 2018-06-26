### Installation

## Pre-requirements (for DEVELOPMENT mode) -- all of these must be installed globally, which means you might need to use sudo.

1. PostgreSQL
2. virtualenv
3. pip
4. pip-tools (only if you want to also make changes)

## Installation step by step

1. Create a new user and a db in Postgres, using the credentials/db name from `settings.py`
    $ createuser -P -e parkinguser   (with password pass)
    $ createdb -e electricitydb -O parkinguser
Just to make sure that everything will run smooth in the following steps, it is best to also install some extensions now:
    $ psql -c 'create extension hstore;' -d parkingdb
    $ psql -c 'create extension unaccent;' -d parkingdb
