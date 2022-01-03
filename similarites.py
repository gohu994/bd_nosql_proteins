from neo4j import data
import pandas as pd
import numpy as np
from datetime import datetime
from csv import writer
import os

def compute_matrix(output_matrix_path):
    start_time = datetime.now()

    brut = pd.read_csv('datas/tostestas.tab', sep='\t', keep_default_na=False)
    domains = brut["Crossreference"].str.split(';')
    dataset = pd.DataFrame({'Entry': brut["Entry"], 'Domains': domains[:]})
    #dataset.index = dataset["Entry"]
    print(dataset)

    stageDSCreated_time = datetime.now()
    print('Création du dataset : ', stageDSCreated_time - start_time, ' (hh:mm:ss.ms)')

    def compare(protA,protB):
        pA = list(protA)
        pB = list(protB)
        if pA[0] != '' and pB[0] != '':
            #entrée : liste des domaines de 2 protéines A et B
            prota = pA
            protb = pB

            union = list(set(prota[0:-1]) | set(protb[0:-1]))
            intersection = list(set(prota[0:-1]) & set(protb[0:-1]))

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


    protname = "P5"
    mat = computeMatriceSimilarites(dataset, protname)[0]
    mat[0] = protname
    print(mat[0])
    #print("qsgqsghqshqfshqsfh",list(mat[0]))
    #print(list(dataset["Entry"]))
    
    
    if os.path.isfile("datas/matrix_tri.csv"):
        # fichier existe
        # ajouter une line au fichier
        file = pd.read_csv('datas/matrix_tri.csv', sep=',', keep_default_na=False)
        # check if line exist
        if not (file.index == protname).any():
            append_list_as_row('datas/matrix_tri.csv', list(mat))
    else:
        # fichier existe pas        
        append_list_as_row('datas/matrix_tri.csv', list(dataset["Entry"]))
        append_list_as_row('datas/matrix_tri.csv', list(mat))
        

compute_matrix("datas/matrix_tri.csv")