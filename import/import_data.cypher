// ID should be unique
CREATE CONSTRAINT user_id_unique ON (n:User) ASSERT n.userId IS UNIQUE;
USING PERIODIC COMMIT 100
LOAD CSV WITH HEADERS FROM 'file:///data.csv.zip' AS row
// create node from info in first few columns
MERGE (u:User:Named {userId: row.id, userName: row.screenName})
// create relationships to all friends, as listed in row, creating nodes as need be as we go
FOREACH (friend in split(trim(replace(replace(row.friends, "]", ""), "[", "")), " ") |
    MERGE (v:User {userId: friend})
    MERGE (u)-[:HAS_FRIEND]->(v)
);
