from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687")
session = driver.session()
print("connected.")

q = """
LOAD CSV WITH HEADERS FROM 'file:///test.tab' AS l FIELDTERMINATOR '\t'
CREATE (n:TESTFROMPYTHON{entry:toString(l.Entry), cross:l.Crossreference});
"""

results = session.run(q).data()
