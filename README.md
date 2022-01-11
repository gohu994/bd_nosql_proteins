# NoSQL Proteins

This project is the backend made using python3.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Just clone this project.

```
git clone git@github.com:gohu994/bd_nosql_proteins.git
```

or

```
git clone https://github.com/gohu994/bd_nosql_proteins.git
```

### Create the neo4j database
In another terminal run to setup the database.

```shell
docker run 	--publish=7474:7474 --publish=7687:7687 	--volume=$HOME/neo4j/data:/data  --volume=$HOME/neo4j/import:/import  --env NEO4J_dbms_memory_pagecache_size=2G  --env=NEO4J_AUTH=none  neo4j
```

### Installing

Installing dependencies.

```
python -m pip install -r requirements.txt
```

### Running
Running the project. 

```
python api.py
```

## API documentation
- POST /protein
- GET /stats
- DELETE /clean 

## Util commands

### Load a csv in neo4j 

```neo4j
LOAD CSV WITH HEADERS FROM 'file:///test.tab' AS l FIELDTERMINATOR '\t'
CREATE (n:PRO{entry:toString(l.Entry), cross:l.Crossreference});
```

### Print a Prot and its similarities links BY ENTRY (1 neighbour depth)
## Care about adding LIMIT to your queries...

```neo4j
MATCH (p:Prot {entry: 'P1'})-[:SIMILARITE]-(prot)
RETURN prot,p
```

### Print a Prot and its similarities links BY ENTRY (2 neighbour depth)
## Care about adding LIMIT to your queries...

```neo4j
MATCH (prot0: Prot{entry: 'P1'})-[:SIMILARITE]-(prot1)
MATCH (prot1)-[:SIMILARITE]-(prot2)
RETURN prot0,prot1,prot2 LIMIT 15

```

### Print a Prot and its similarities links BY PROTEIN NAME
(You need to have protein names inserted in your graph for this to work). Care about adding LIMIT to your queries...

```neo4j
MATCH (p:Prot {name: 'Protein Name 1'})-[:SIMILARITE]-(prot)
RETURN prot,p
```

### Print the number of isolated proteins

MATCH (p:Protein)
WHERE NOT (p)-[:SIMILARITE]-(:Protein)
RETURN COUNT(p) AS isolatedProteins

### Check number of existing relationships of given prot with threshold
MATCH p=(:Prot {entry: 'P4'})<-[r:SIMI]->() WHERE r.value[0] >= 0.5 RETURN count(p)

## Authors

* **Damien ETHÈVE**
* **Hugo BENAMEUR**
* **Steson TANG**
* **Maxime NEVEUX** 


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details