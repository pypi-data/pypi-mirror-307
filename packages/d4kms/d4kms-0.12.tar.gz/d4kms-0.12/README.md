# Introduction
This read me identifies a set of microservices that implement a range of functionality that allows for the handling of clinical trial data in an automated manner. The use cases addressed are

1. Import of data held in a variety of data formats into study designs
1. Export of data in a number of formats

The microservices within the system are:

1. Registration Authority
1. Clinical Recording Model
1. Controlled Terminology
1. Biomedical Concepts
1. SDTM
1. Forms
1. Study

The services are all python services running on FastAPI and uvicorn. They can be run locally using a single shared Neo4j instance or deployed. When deployed each micorservices requires a separate Aura Neo4j instance.

# Running Locally

Use a single Neo4 instance will all databases for the microservices setup within one instance. Typical names for a devlepoment environment are

- ra-service-dev
- crm-service-dev
- bc-service-dev
- sdtm-service-dev
- study-service-dev
- form-service-dev

Note: there are no separate data bases for Study Import service or the Study Data Import service

## Port Numbers

### User Interface Services

| Microservice | Port |
| ------------- | ------------- |
| CT | 8000 |
| BC | 8001 |
| Study | 8002 |
| Form | 8003 |
| SDTM | 8004 |

### Data Services

| Microservice | Port |
| ------------- | ------------- |
| RA | 8010 |
| CRM | 8011 |
| CT | 8012 |
| BC | 8013 |
| Study | 8014 |
| Study Import | 8015 |
| Form | 8016 |
| SDTM | 8017 |
| Study Data Import | 8018 |

### To Run

Use the ```microservice.command``` file to run. Note this file is mac specific. This will start all of the services and the UIs. There is also a dev_server.sh file in each git repo to run each element individually.

# Deployed

## Overview

To deploy each microservice the following actions should be followed.

1. Create Aura Neo4j instance.
1. Load the data using the data prep utility
1. Deploy the microservice
1. Check all running

## Neo4j Aura

Use the Aura console to create the database as per the site instructions. Download the file holding the credentials (username and password) for the instance

## Data Load

### Overview

From the appropriate data prep project

1. Setup the virtual environment
1. Set the environment variables for the credentials of the neo4j instance
1. Set production
1. Run the load python file

### Virtual Environment

Run ```. ./setup_env.sh```

### Environment Variables

Modify the .production_env file. The file will need to contain the following lines

```
NEO4J_URI=<database uri>
NEO4J_DB_NAME=neo4j
NEO4J_USERNAME=<username>
NEO4J_PASSWORD=<password>
GITHUB=<URL of the github repo main page>
```

The database URI will look something like ```neo4j+s://a1bc23d4.databases.neo4j.io```
The githb repo URL will look something like ```https://raw.githubusercontent.com/data4knowledge/ra_prep/main/```

### Set Production

We need to tell the load utility to use the production database rather than the local (development) one. This is done via setting the ```PYTHON_ENVIRONMENT```environment variable. To so this run ```. ./set_production.sh```

### Load Data

There will be a python rpogram to load the data. It will be named ```stage_<n>_load.py```. Run this program by entering ```python stage_2_load.py```, here n is 2.

The output from the program should look somethig like

```
Deleting database ...
Database deleted. Load new data ...
https://raw.githubusercontent.com/data4knowledge/ra_prep/main/load_data/node-namespace-1.csv
https://raw.githubusercontent.com/data4knowledge/ra_prep/main/load_data/relationship-manages-1.csv
https://raw.githubusercontent.com/data4knowledge/ra_prep/main/load_data/node-registration_authority-1.csv
<Record file='progress.csv' source='file' format='csv' nodes=9 relationships=7 properties=58 time=4294 rows=0 batchSize=-1 batches=0 done=True data=None>
Load complete. 9 nodes and 7 relationships loaded in 4294 milliseconds.
```

## Deploy Microservice

The microservices are deployed using the fly.io cloud service. 

1. General python instructions are available here https://fly.io/docs/languages-and-frameworks/python/
1. Installing the fly command line tool is detailed here https://fly.io/docs/hands-on/install-flyctl/ 
1. deploy the app
1. Set environment variables

### Environment Variables

Setting environment variables on the server is achieved by using th ecommand line program, either one at a time

```fly secrets set SUPER_SECRET_KEY=password1234```

or multiple values, note space delimited

```fly secrets set NEO4J_URI=xxx NEO4J_PASSWORD=yyy```

# Using Auth0 by Okta

## Environment Keys

```
AUTH0_SESSION_SECRET=<session secret key>
AUTH0_DOMAIN=<from the Auth0 configuation>
AUTH0_CLIENT_ID=<from the Auth0 configuation>
AUTH0_CLIENT_SECRET=<from the Auth0 configuation>
AUTH0_AUDIENCE=<from the Auth0 configuation>
AUTH0_MNGT_CLIENT_ID=<Management API client ID>
AUTH0_MNGT_CLIENT_SECRET=<Management API client secret>
ROOT_URL=<base URL for the app>
```

For the session secret run ```cat /dev/urandom | LC_ALL=C tr -dc 'a-zA-Z0-9' | fold -w 50 | head -n 1```to generate a 50 character randon string

For the root URL use ```http:\\localhost:8000```or similar for a locally running app or ```https:\\xxx.fly.dev```for a deployed app

## Code in Main Program

Use this initialisation code

```
authorisation = Auth0Service(app)
authorisation.register()
```

Need a local method to protect an endpoint

```
def protect_endpoint(request: Request) -> None:
  authorisation.protect_route(request, "/login")
```

and then protect an endpoint by using

```
@app.get("/index", dependencies=[Depends(protect_endpoint)])
def index(request: Request):
  ...code...
```

# Loading Studies & Data

To be defined.

# Building package

## Build and Upload

Use pip to install build and twine. Use the following commands to build

```python -m build``` 

and upload to pypi.org using the command

```twine upload dist/*``` 

Upload requires a token.

## Token

Generate an API token on pypi.org. Then, to use the API token:

```
Set your username to __token__
Set your password to the token value, including the pypi- prefix
```