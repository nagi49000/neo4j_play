USING PERIODIC COMMIT 100
LOAD CSV WITH HEADERS FROM 'file:///data.csv' AS row
MERGE (u:User {userId: row.id, userName: row.screenName});
