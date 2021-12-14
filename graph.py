from neo4j import GraphDatabase
import pandas as pd
import numpy as np

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
	q = """
	LOAD CSV WITH HEADERS FROM 'file:///test.tab' AS l FIELDTERMINATOR '\t'
	CREATE (n:Protein{entry:toString(l.Entry), cross:l.Crossreference});
	"""

	results = session.run(q).data()

"""
Ouvrir matrix_tri.csv (similarites) en DataSet
Parcourir chaque paire (si similarite =/= 0 => requete neo4j)
Requete neo4j de creation du lien
"""

def createSim():

	qDel = "MATCH (a:Protein)-[r:SIMILARITE]->(b:Protein) DELETE r"
	session.run(qDel).data()

	similarites = pd.read_csv("datas/matrix_tri.csv")

	serie = dm_to_series1(similarites)

	for column in similarites:
		for index, row in similarites.iterrows():
			if (column==index):
					break
			if (row[column]>0):
				print(column)
				print(index)
				print(row[column])
				#q="CREATE (Protein:"+column+")-[r:SIMILARITE]->(Protein:"+index+")"
				#q="MATCH (a:Prot), (b:Prot) WHERE a.entry = '"+str(index)+"' AND b.entry = '"+str(column)+"' CREATE (a)-[r:"+str(row[column])+"]->(b) RETURN type(r)"
				q="MATCH (a:Protein {entry: \""+str(index)+"\"}) MATCH (b:Protein {entry:\""+str(column)+"\"}) MERGE (a)-[rel:SIMILARITE {value:["+str(row[column])+"]}]-(b) RETURN rel;"
				print (q)
				results = session.run(q).data()


"""
Input depuis la ligne de commande :
- 0 pour recreer la DB
- 1 pour la remplir avec les similarites
"""

print("Recreer DB : 0, similarite DB : 1")
input = input()
if (input=="0"):
	q="MATCH (n:Protein) detach delete n"
	results = session.run(q).data()
	create()
elif (input=="1"):
	createSim()