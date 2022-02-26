#!/bin/bash
rm -rf /data/transactions/neo4j
rm -rf /data/databases/neo4j
neo4j-admin import --database=neo4j --skip-duplicate-nodes --skip-bad-relationships --nodes=User=import-source-nodes-headers.csv,import-source-nodes.*.csv.tar.gz --nodes=User=import-target-nodes-headers.csv,import-target-nodes.*.csv.tar.gz --relationships=HAS_FRIEND=import-relationships-headers.csv,import-relationships.*.csv.tar.gz
