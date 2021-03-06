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
	q = """
		LOAD CSV WITH HEADERS FROM 'file:///fulldata.tab' AS l FIELDTERMINATOR '\t'
		CREATE (n:Prot{entry:toString(l.Entry), cross:l.CrossReference, name:l.ProteinNames, ecNumber:l.ECnumber, geneOntology: l.GeneOntology});

	"""
	results0 = session.run(q).data()


def delete():
	q0 = """
	MATCH (n:Prot) detach delete n;
	"""
	results0 = session.run(q0).data()
"""
Ouvrir matrix_tri.csv (similarites) en DataSet
Parcourir chaque paire (si similarite =/= 0 => requete neo4j)
Requete neo4j de creation du lien
"""


def createAllSim():

	qDel = "MATCH (a:Prot)-[r:SIMI]->(b:Prot) DELETE r"
	session.run(qDel).data()

	similarites = pd.read_csv("datas/matrix_tri.csv")

	for column in similarites:
		for index, row in similarites.iterrows():
			if (column==index):
					break
			if (row[column]>0):
				#q="CREATE (Protein:"+column+")-[r:SIMI]->(Protein:"+index+")"
				#q="MATCH (a:Prot), (b:Prot) WHERE a.entry = '"+str(index)+"' AND b.entry = '"+str(column)+"' CREATE (a)-[r:"+str(row[column])+"]->(b) RETURN type(r)"
				q="MATCH (a:Prot {entry: \""+str(index)+"\"}) MATCH (b:Prot {entry:\""+str(column)+"\"}) MERGE (a)-[rel:SIMI {value:["+str(row[column])+"]}]-(b) RETURN rel;"
				print (q)
				results = session.run(q).data()

def createSim(prot, seuil):
	print("seuil : ", seuil)
	similarites_csv = pd.read_csv("datas/matrix_tri.csv")
	alone = True
	# il faut lister les protéines similaires
	try:
		similarites = similarites_csv.loc[prot]
		header = list(similarites_csv.columns)
		#print("loc : \n", similarites.loc[prot], "\n")
		for head in header:
			if head != prot and similarites.loc[head] > seuil:
				alone = False
				q="MATCH (a:Prot {entry: \"" + head + "\"}) MATCH (b:Prot {entry:\"" + prot + "\"}) MERGE (a)-[rel:SIMI {value:[" + str(
						similarites.loc[head]) + "]}]-(b) RETURN rel;"
				results = session.run(q).data()
		if alone:
			print('lonely protein' + prot)
			q="MATCH (a:Prot {entry: \"" + head + "\"}) MATCH (b:Prot {entry:\"" + head + "\"}) MERGE (a)-[rel:SIMI {value:[" + str(
				1.0) + "]}]-(b) RETURN rel;"
			results = session.run(q).data()
	except KeyError:
		print("Protéine ",prot," pas trouvée")


	"""for row in similarites:
		print("column : ",row, " / prot : ", prot)
		if (row==prot):
			inside = True

			for index, row in similarites.iterrows():
				print("ind : ",index,row)
				if (index!=row):
					if (row[row] > float(seuil)):
						alone = False
						q="MATCH (a:Prot {entry: \""+str(index)+"\"}) MATCH (b:Prot {entry:\""+str(column)+"\"}) MERGE (a)-[rel:SIMI {value:["+str(row[column])+"]}]-(b) RETURN rel;"
						print (q)
						results = session.run(q).data()
			if alone:
				print('lonely protein' + prot)
				q = "MATCH (a:Prot {entry: \"" + prot + "\"}) MATCH (b:Prot {entry:\"" + prot + "\"}) MERGE (a)-[rel:SIMI {value:[" + str(1.0) + "]}]-(b) RETURN rel;"
				results = session.run(q).data()
"""

def createSimWithoutCSV(similarites,proteines,prot, seuil):
	"""
	:param similarites: liste de la similarité d'une protéine avec toutes les autres
	:param proteines: liste de toutes les protéines
	:param prot: nom de la protéine demandée
	:param seuil: seuil
	"""
	print("seuil : ", seuil)
	alone = True
	try:
		header = proteines
		for i in range(len(header)):
			head = header[i]
			#print(i,prot,head,similarites[i],float(seuil), alone)
			if head != prot and float(similarites[i]) > float(seuil):
				q_0 = "MATCH p=(:Prot {entry: '" + head + "'})-[r:SIMI]-() WHERE r.value[0] > " + str(seuil) + " RETURN count(p)"
				res_0 = session.run(q_0).data()[0]['count(p)']
				#print('OK')
				alone = False
				if res_0 == 0:
					q="MATCH (a:Prot {entry: \"" + head + "\"}) MATCH (b:Prot {entry:\"" + prot + "\"}) MERGE (a)-[rel:SIMI {value:[" + str(
							similarites[i]) + "]}]->(b) RETURN rel;"
					results = session.run(q).data()
		#print(alone)
		if alone:
			print('lonely protein ' + prot)
			q="MATCH (a:Prot {entry: \"" + head + "\"}) MATCH (b:Prot {entry:\"" + head + "\"}) MERGE (a)-[rel:SIMI {value:[" + str(
				1.0) + "]}]-(b) RETURN rel;"
			results = session.run(q).data()
	except KeyError:
		print("Protéine",prot,"pas trouvée")
