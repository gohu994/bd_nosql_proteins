# NoSQL Proteins

## Installation

```bash
$ pip install -r requirements.txt
```

## Create the neo4j database
```shell
docker run 	--publish=7474:7474 --publish=7687:7687 	--volume=$HOME/neo4j/data:/data  --volume=$HOME/neo4j/import:/import  --env NEO4J_dbms_memory_pagecache_size=2G  --env=NEO4J_AUTH=none   neo4j
```

## Run

```bash
$ python main.py
```





## Load a csv in neo4j 

```neo4j
LOAD CSV WITH HEADERS FROM 'file:///test.tab' AS l FIELDTERMINATOR '\t'
CREATE (n:PRO{entry:toString(l.Entry), cross:l.Crossreference});
```

