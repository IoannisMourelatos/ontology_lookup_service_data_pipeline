# ontology_lookup_service_data_pipeline
IAI Data Engineering Assessment

## Requirements

* [Docker](https://www.docker.com/).
* [Docker Compose](https://docs.docker.com/compose/install/).
* [Make](http://gnuwin32.sourceforge.net/packages/make.htm).

## Local setup development

* Build the image:

```
make build-img
```

* Start the stack with make:

```
make compose-up
```

* Initialize the database through the migration:

```
make migrate
```

JSON based web API based on FastAPI: http://localhost:8000/docs/

PGAdmin, PostgreSQL web administration: http://localhost:5050

Usernames and passwords stored in the .env file.

* To shut down the stack:

```
make compose-down
```
