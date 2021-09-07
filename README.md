# Setup MongoDB for ML
This helps you configure MongoDB for storing your ML data (to move from pure pandas).

## Links to files
- [Makefile with all commands](Makefile)
- [Docker-compose configuration (no authentication)](Makefile)
- [Python library (ml_mongo.py)](ml_mongo.py)
- [Python example usage](example.py)
- [Additional: pymongo tutorial](https://pymongo.readthedocs.io/en/stable/tutorial.html)
- [Additional: mongodb base concept and shell syntax](https://docs.mongodb.com/manual/crud/)


## Installation and usage

### Install `Docker` and `docker-compose` (skip if already installed)

    make install-docker

### Start Database

    make up

### Install python requirements

    make install-requirements-py

### Run example

    make example-populate  # This populates mongo database from csv file (using pandas)
    make example-filter    # Filter docs by a condition
    make example-insert    # Insert a doc
    make example-remove    # Filter and remove docs
    make db-browse         # Opens mongo-express dashboard to browse or modify your data

### Remove all data
    
    make db-flush

### Stop database

    make down

### Connect database, using Mongo Shell (for advanced users)

    make db-shell
