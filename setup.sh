sudo rm -rf ~/neo4j

docker run -d --publish=7474:7474 --publish=7687:7687 --volume=$HOME/neo4j/data:/data  --volume=$HOME/neo4j/import:/import  --env NEO4J_dbms_memory_pagecache_size=2G  --env=NEO4J_AUTH=none   neo4j

sudo cp ./datas/fulldata.tab ~/neo4j/import

python3 api.py