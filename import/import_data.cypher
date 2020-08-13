CREATE CONSTRAINT user_id_unique ON (n:User) ASSERT n.id IS UNIQUE;
USING PERIODIC COMMIT 100
LOAD CSV WITH HEADERS FROM 'file:///data.csv.zip' AS row
MERGE (u:User:Named {userId: row.id, userName: row.screenName});
