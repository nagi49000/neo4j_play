# neo4j_play

Data from https://www.kaggle.com/hwassner/TwitterFriends?select=data.csv

Neo4j docker-compose set up from https://medium.com/@thibaut.deveraux/how-to-install-neo4j-with-docker-compose-36e3ba939af0

## Loading data into an active database

Data and import cypher are mounted in /import . On
```
docker-compose up
```
a neo4j server will be available, with an empty database, with default auth.

Once the server is up, you can navigate to the neo4j browser on http://localhost:7474/browser/ from your favourite web browser. From there, you can connect to the default database with username "neo4j" and password "neo4j". The browser will ask you to change password (the docker-compose environment assumes this will be "neo").

To import the twitter friends data, one can exec into the running shell
```
docker exec -it neo4j_play_neo4j_1 /bin/bash
```
cd into /import, and run (which, under the hood, uses neo4j's LOAD CSV)
```
cypher-shell -f import_data.cypher
```
After import, the data will be available to see in the neo4j browser. As a simple example to check import, one can run the cypher query
```
MATCH(n) RETURN COUNT(n);
```
in the top bar of the browser.