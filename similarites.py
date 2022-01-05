from neo4j import data
import pandas as pd
import numpy as np
from datetime import datetime
from csv import writer
import os

from pandas.core.frame import DataFrame

def compute_matrix(protName):
    start_time = datetime.now()

    brut = pd.read_csv('datas/tostestas.tab', sep='\t', keep_default_na=False)
    domains = brut["Cross_reference"].str.split(';')

    dataset = pd.DataFrame({'Entry': brut["Entry"], 'Domains': domains[:]})
    #dataset.index = dataset["Entry"]
    print(dataset)

    stageDSCreated_time = datetime.now()
    print('Création du dataset : ', stageDSCreated_time - start_time, ' (hh:mm:ss.ms)')

    def compare(protA,protB):
        pA = list(protA)
        pB = list(protB)
        print(pA)
        print(pB)
        if pA[0] != '' and pB[0] != '':
            #entrée : liste des domaines de 2 protéines A et B
            prota = pA
            protb = pB

            union = list(set(prota[0:len(prota)]) | set(protb[0:len(protb)]))
            intersection = list(set(prota[0:len(prota)]) & set(protb[0:len(protb)]))

            return (len(intersection)/len(union))
        else:
            return 0

    def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
        with open(file_name, 'a+', newline='') as write_obj:
            # Create a writer object from csv module
            csv_writer = writer(write_obj)
            # Add contents of list as last row in the csv file
            csv_writer.writerow(list_of_elem)
        
    def computeMatriceSimilarites(dataset, protName):
        nomsProteines = list(dataset['Entry'])
        #print(nomsProteines.index(protName))
        matrice = np.zeros((1,len(nomsProteines)+1), dtype=object) # np.zeros(nb lignes, nb colonnes)
        #print(matrice)
        #for i in range(len(nomsProteines)):
        #index = dataset.loc[protName, :]
        #print("INDEX", index)
        index = nomsProteines.index(protName)
        print("Index: ",index)
        matrice[0][nomsProteines.index(protName)] = protName
        print(matrice[0])
        for j in range(0,len(nomsProteines)):
            temp = compare(dataset['Domains'][index],dataset['Domains'][j])
            matrice[0][j+1] = temp
            #matrice[j][0+1] = temp
        #print(0, '/', len(nomsProteines), ' proteins treated')
        return matrice

    protname = protName
    mat = computeMatriceSimilarites(dataset, protname)[0]
    mat[0] = protname
    
    # calculer similatité des voisins
    entries=list(dataset["Entry"])
    matx=list(mat)
    lstSimilaire = []
    cpt = 0
    for i in matx:
        if i != 0 and i != protname and i != 1: #  
            lstSimilaire.append(entries[cpt-1])
            #print(cpt-1) # c'est l'index qui selectionne les proteine similaire
        cpt += 1
    print(lstSimilaire)
    
    if os.path.isfile("datas/matrix_tri.csv"):
        # fichier existe
        # ajouter une line au fichier
        file = pd.read_csv('datas/matrix_tri.csv', sep=',', keep_default_na=False)
        # check if line exist
        if not (file.index == protname).any():
            append_list_as_row('datas/matrix_tri.csv', list(mat))

            for name in list(lstSimilaire):
                print("NAME : ",name)
                mat2 = computeMatriceSimilarites(dataset, name)[0]
                mat2[0] = name
                if not (file.index == name).any():
                    append_list_as_row('datas/matrix_tri.csv', list(mat2))
                
    else:
        # fichier existe pas        
        append_list_as_row('datas/matrix_tri.csv', list(dataset["Entry"]))
        append_list_as_row('datas/matrix_tri.csv', list(mat))
        file = pd.read_csv('datas/matrix_tri.csv', sep=',', keep_default_na=False)
        
        print(list(lstSimilaire))
        for name in list(lstSimilaire):
            print("NAME : ",name)
            mat2 = computeMatriceSimilarites(dataset, name)[0]
            mat2[0] = name
            if not (file.index == name).any():
                append_list_as_row('datas/matrix_tri.csv', list(mat2))
    
    
    

