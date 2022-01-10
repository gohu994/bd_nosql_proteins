from neo4j import GraphDatabase
import pandas as pd
import numpy as np

import sys

driver = GraphDatabase.driver("bolt://localhost:7687")
session = driver.session()
print("connected.")

def dm_to_series1(df):
    df = df.astype(float)
    df.values[np.triu_indices_from(df, k=1)] = np.nan
    return df.unstack().dropna()


"""
Requete de creation du fichier 
=> Copier le fichier .tab dans neo4j/import
"""

def create():
  
	q1 = """
		MATCH (n) detach delete n;
	"""

	q = """
		LOAD CSV WITH HEADERS FROM 'file:///fulldata.tab' AS l FIELDTERMINATOR '\t'
		CREATE (n:Prot{entry:toString(l.Entry), cross:l.Crossreference});
	"""

	results = session.run(q1).data()
	results = session.run(q).data()

"""
Ouvrir matrix_tri.csv (similarites) en DataSet
Parcourir chaque paire (si similarite =/= 0 => requete neo4j)
Requete neo4j de creation du lien
"""

def createSim(seuil):

	qDel = "MATCH (a:Prot)-[r:SIMI]->(b:Prot) DELETE r"
	session.run(qDel).data()

	similarites = pd.read_csv("datas/matrix_tri.csv")

	serie = dm_to_series1(similarites)

	for column in similarites:
		for index, row in similarites.iterrows():
			if (column==index):
					break
			if (row[column]>= float(seuil)):
				#print(column)
				#print(index)
				#print(row[column])
				#q="MATCH (a:Prot), (b:Prot) WHERE a.entry = '"+str(index)+"' AND b.entry = '"+str(column)+"' CREATE (a)-[r:"+str(row[column])+"]->(b) RETURN type(r)"
				q="MATCH (a:Prot {entry: \""+str(index)+"\"}) MATCH (b:Prot {entry:\""+str(column)+"\"}) MERGE (a)-[rel:SIMI {value:["+str(row[column])+"]}]-(b) RETURN rel;"
				#print (q)
				results = session.run(q).data()

