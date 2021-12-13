from py2neo import Graph

def graph_creation():
    uri = "neo4j://localhost:7687/neo4j"
    graph = Graph(uri, auth=("neo4j", "password"))
    print('SUCCESS: Connected to the Neo4j Database.')


    result = graph.run('LOAD CSV WITH HEADERS FROM "file:///matrix.csv" AS matrix'
              'CREATE (p:Prtein {id:matrix[0], name:matrix[0]});')

    print(result)
    """tx.run('load csv with headers from "file:///datas/matrix.csv" as matrix '
           'with matrix'
           'FOREACH prot IN CASE WHEN '
           'create (p:Protein{'
           'id:matrix[0],name:matrix[0],full_name:matrix[0],'
           '});')"""

graph_creation()