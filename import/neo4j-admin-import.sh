#!/bin/bash
rm -rf /data/transactions/kaggle
rm -rf /data/databases/kaggle
neo4j-admin import --database=kaggle --skip-duplicate-nodes --skip-bad-relationships --nodes=User=import-source-nodes-headers.csv,import-source-nodes.*.csv.tar.gz --nodes=User=import-target-nodes-headers.csv,import-target-nodes.*.csv.tar.gz --relationships=HAS_FRIEND=import-relationships-headers.csv,import-relationships.*.csv.tar.gz
