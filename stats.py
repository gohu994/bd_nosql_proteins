from neo4j import GraphDatabase
import pandas as pd
import numpy as np

import sys

driver = GraphDatabase.driver("bolt://localhost:7687")
session = driver.session()
print("connected.")

def getNumberIsolated():
	q="MATCH (p:Prot) WHERE NOT (p)-[:SIMILARITE]-(:Prot) RETURN COUNT(p) AS isolatedProteins"
	results = session.run(q).data()
	print(results)

def getNumberLinked():
	q="MATCH (p:Prot) WHERE (p)-[:SIMILARITE]-(:Prot) RETURN COUNT(p) AS linkedProteins"
	results = session.run(q).data()
	print(results)

def getNumberLabelled():
	q="MATCH (p:Prot) WHERE p.ec IS NOT NULL OR p.go IS NOT NULL RETURN COUNT(p) AS labelledProteins"
	results = session.run(q).data()
	print(results)

def getNumberUnlabelled():
	q="MATCH (p:Prot) WHERE p.ec IS NULL AND p.go IS NULL RETURN COUNT(p) AS unlabelledProteins"
	results = session.run(q).data()
	print(results)


def countDomains():
	q="MATCH (p:Prot) RETURN p LIMIT 25"
	results = session.run(q).data()
	count = []
	for k in results:
		try:
			# si le tableau count ne possède pas encore l'emplacement accueillant
			# le nombre de domaine de la protéine évalué dans la boucle)
			while (k["p"]["cross"].count(";")+1>=len(count)):
				count.append(0)
			count[k["p"]["cross"].count(";")+1]=count[k["p"]["cross"].count(";")+1]+1
		except KeyError:
			count[0]=count[0]+1
	for i in range(len(count)):
		print(i,"domaines :",count[i])

"""
Input depuis la ligne de commande :
- 0 pour le nombre de protéines isolées
- 1 pour la remplir avec les similarites
"""

print("Nombre de protéines isolées / linkées : 0, Nombre de protéines labellées / non-labellées : 1, Compte des protéines par nombre de domaines : 2")
input = input()
if (input=="0"):
	getNumberIsolated()
	getNumberLinked()
elif (input=="1"):
	getNumberLabelled()
	getNumberUnlabelled()
elif (input=="2"):
	countDomains()