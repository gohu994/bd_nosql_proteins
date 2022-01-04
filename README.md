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

## Print a Prot and its similarities links BY ENTRY (1 neighbour depth)
## Care about adding LIMIT to your queries...

```neo4j
MATCH (p:Prot {entry: 'P1'})-[:SIMILARITE]-(prot)
RETURN prot,p
```

## Print a Prot and its similarities links BY ENTRY (2 neighbour depth)
## Care about adding LIMIT to your queries...

```neo4j
MATCH (p:Prot {entry: 'P1'})-[:SIMILARITE]-(prot)-[:SIMILARITE]-(prot2)
RETURN prot,prot2,p LIMIT 15

```

## Print a Prot and its similarities links BY PROTEIN NAME
## (You need to have protein names inserted in your graph for this to work)
## Care about adding LIMIT to your queries...

```neo4j
MATCH (p:Prot {name: 'Protein Name 1'})-[:SIMILARITE]-(prot)
RETURN prot,p
```

## Print the number of isolated proteins

MATCH (p:Protein)
WHERE NOT (p)-[:SIMILARITE]-(:Protein)
RETURN COUNT(p) AS isolatedProteins
