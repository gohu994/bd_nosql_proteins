from neo4j import GraphDatabase
import pandas as pd
import numpy as np

import os.path

driver = GraphDatabase.driver("bolt://localhost:7687")
session = driver.session()

def getNumberIsolated():
	q="MATCH (p:Prot) WHERE NOT (p)-[:SIMI]-(:Prot) RETURN COUNT(p) AS isolatedProteins"
	results = session.run(q).data()
	return results[0].get("isolatedProteins")

def getNumberLinked():
	q="MATCH (p:Prot) WHERE (p)-[:SIMI]-(:Prot) RETURN COUNT(p) AS linkedProteins"
	results = session.run(q).data()
	return results[0].get("linkedProteins")


def getNumberLabelled():
	q="MATCH (p:Prot) WHERE p.ecNumber IS NOT NULL OR p.geneOntology IS NOT NULL RETURN COUNT(p) AS labelledProteins"
	results = session.run(q).data()
	return results[0].get("labelledProteins")

def getNumberUnlabelled():
	q="MATCH (p:Prot) WHERE p.ecNumber IS NULL AND p.geneOntology IS NULL RETURN COUNT(p) AS unlabelledProteins"
	results = session.run(q).data()
	return results[0].get("unlabelledProteins")

def getNumberCompiled():
	if os.path.isfile("datas/matrix_tri.csv"):
		df = pd.read_csv("datas/matrix_tri.csv")
		print(len(df),len(df.columns))
		return round(len(df)*100/len(df.columns),2)
	else:
		return 0

def countDomains():
	q="MATCH (p:Prot) RETURN p"
	results = session.run(q).data()
	count = [0]
	for k in results:
		try:
			# si le tableau count ne possède pas encore l'emplacement accueillant
			# le nombre de domaine de la protéine évalué dans la boucle)
			while (k["p"]["cross"].count(";")>=len(count)):
				count.append(0)
			count[k["p"]["cross"].count(";")]=count[k["p"]["cross"].count(";")]+1
		except KeyError:
			count[0]=count[0]+1
	for i in range(len(count)):
		print(i,"domaines :",count[i])
	return count
