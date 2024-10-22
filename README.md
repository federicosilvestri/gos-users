# Go Out Safe - users

[![Build Status](https://travis-ci.com/federicosilvestri/ase-GoOutSafe-s4.svg?token=wrPAra8ynq6rYZess6c1&branch=master)](https://travis-ci.com/federicosilvestri/ase-GoOutSafe-s4)
![codecov](https://codecov.io/gh/federicosilvestri/ase-GoOutSafe-s4/branch/master/graph/badge.svg?token=WN7CJ8Q74F)

This is the source code of GoOutSafe application, self
project of *Advanced Software Engineering* course,
University of Pisa.
 
## Team info

- The *squad id* is **4**
- The *team leader* is *TBD*

#### Members

|Name and Surname    | Email                         |
|--------------------|-------------------------------|
|*Federico Silvestri*|f.silvestri10@studenti.unipi.it|
|Leonardo Calamita   |l.calamita@studenti.unipi.it   |
|*Chiara Boni*       |c.boni5@studenti.unipi.it      |
|Nunzio Lopardo      |n.lopardo@studenti.unipi.it    |
|*Paolo Murgia*      |p.murgia1@studenti.unipi.it    |


## Instructions

### Initialization

To setup the project initially you have to run these commands
inside the project's root.

`virtualenv -p python3 venv`

`source venv/bin/activate`

`pip install -r requirements.dev.txt`

### Run the project

To run the project you have to setup the flask environment,
you can do it by executing the following commands:

```shell script
cp env_file_example env_file
cp env_file_example .env
docker-compose up redis
export FLASK_ENV=development
flask run
```


#### Application Environments

The available environments are:

- debug
- development
- testing
- production

If you want to run the application with development environment
you can run the `run.sh` script.


### Apply migrations

If you change something in the models package or you create a new model,
you have to run these commands to apply the modifications:

`flask db migrate -m '<message>'`

and
 
`flask db upgrade`

### Run tests

To run all the tests, execute the following command:

`python -m pytest`

You can also specify one or more specific test files, in order to run only those specific tests.
In case you also want to see the overall coverage of the tests, execute the following command:

`python -m pytest --cov=gooutsafe`

In order to know what are the lines of codes which are not covered by the tests, execute the command:

`python -m pytest --cov-report term-missing`

## Conventions

- Name of files must be snake_cased
- Name of methods, properties, variables must be snake_cased
- Name of classes must be PascalCased 
- Name of constants must be UPPERCASE 
- The class name of managers must be in the format `<BeanName>Manager`

### Future implementations

- [Checking phone numbers](https://pypi.org/project/phonenumbers/)
