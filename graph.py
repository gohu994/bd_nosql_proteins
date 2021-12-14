from neo4j import GraphDatabase
import pandas as pd
import numpy as np

def dm_to_series1(df):
    df = df.astype(float)
    df.values[np.triu_indices_from(df, k=1)] = np.nan
    return df.unstack().dropna()


driver = GraphDatabase.driver("bolt://localhost:7687")
session = driver.session()
print("connected.")

"""
Requete de creation du fichier 
=> Copier le fichier .tab dans neo4j/import
"""

q = """
LOAD CSV WITH HEADERS FROM 'file:///tostestas.tab' AS l FIELDTERMINATOR '\t'
CREATE (n:Protein{entry:toString(l.Entry), cross:l.Crossreference});
"""

results = session.run(q).data()

"""
Ouvrir matrix_tri.csv (similarites) en DataSet
Parcourir chaque paire (si similarite =/= 0 => requete neo4j)
Requete neo4j de creation du lien
"""

similarites = pd.read_csv("datas/matrix_tri.csv")

serie = dm_to_series1(similarites)

#print(serie)

for column in similarites:
	for index, row in similarites.iterrows():
		if (column==index):
				break
		if (row[column]>0):
			print(column)
			print(index)
			print(row[column])
			#q="CREATE (Protein:"+column+")-[r:SIMILARITE]->(Protein:"+index+")"
			#q="MATCH (a:Prot), (b:Prot) WHERE a.entry = '"+index+"' AND b.entry = '"+column+"' CREATE (a)-[r:"+row[column]+"]->(b) RETURN type(r)"
			q="MATCH (a:Prot), (b:Prot) WHERE a.entry = "+"\'"+index+"\'"+" AND b.entry = "+"\'"+column+"\'"+" CREATE (a)-[r:"+row[column]+"]->(b) RETURN type(r)"
			print (q)
			#results = session.run(q).data()