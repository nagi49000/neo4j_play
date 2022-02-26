# neo4j_play

Data from https://www.kaggle.com/hwassner/TwitterFriends?select=data.csv

Neo4j docker-compose set up from https://medium.com/@thibaut.deveraux/how-to-install-neo4j-with-docker-compose-36e3ba939af0

## Loading data into an active database

This uses [LOAD CSV](https://neo4j.com/docs/cypher-manual/current/clauses/load-csv/). The bespoke code for this method is all in import_data.cypher.

Data and import cypher are mounted in /import . On
```
docker-compose up
```
a neo4j server will be available, with an empty database, with default auth. To import the twitter friends data, one can exec into the running shell
```
docker exec -it neo4j_play_neo4j_1 /bin/bash
```
cd into /import, and run
```
cypher-shell -f import_data.cypher
```

## Loading data into a non-existent or switched off database

This uses [neo4j-admin-import](https://neo4j.com/docs/operations-manual/current/tutorial/neo4j-admin-import/). The bespoke code for this method is in make-admin-import-files.py and neo4j-admin-import.sh.

The files need to be prepared for import. In the import directory, there is a python script for this, which can be run with
```
python make-admin-import-files.py
```
On
```
docker-compose up
```
a neo4j server will be available, with an empty database, with default auth.
To import the twitter friends data, one can exec into the running shell
```
docker exec -it neo4j_play_neo4j_1 /bin/bash
```
cd into /import, and run, in the /import directory (!this shell script will delete any existing database data!)
```
neo4j-admin-import.sh
```
The database may need to be restarted for the changes to be picked up, which can be performed by restarting the docker container.

## Checking data is loaded

With the server up, the neo4j browser will be available at http://localhost:7474/ with username and password both "neo4j". After import, the data will be available to see in the neo4j browser. As a simple example to check import, one can run the cypher query
```
MATCH(n) RETURN COUNT(n);
```
in the top bar of the browser.
