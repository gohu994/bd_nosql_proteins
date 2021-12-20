import pandas as pd
import numpy as np
from datetime import datetime

def compute_matrix(output_matrix_path):
    start_time = datetime.now()

    brut = pd.read_csv('datas/tostestas.tab', sep='\t', keep_default_na=False)
    domains = brut["Cross_reference"].str.split(';')
    dataset = pd.DataFrame({'Entry': brut["Entry"], 'Domains': domains[:]})

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


    def computeMatriceSimilarites(dataset):
        nomsProteines = list(dataset['Entry'])
        matrice = np.zeros((len(nomsProteines),len(nomsProteines)+1), dtype=object) # np.zeros(nb lignes, nb colonnes)
        for i in range(len(nomsProteines)):
            matrice[i][0] = nomsProteines[i]
            for j in range(i,len(nomsProteines)):
                temp = compare(dataset['Domains'][i],dataset['Domains'][j])
                matrice[i][j+1] = temp
                matrice[j][i+1] = temp
            print(i, '/', len(nomsProteines), ' proteins treated')
        return matrice

    mat = computeMatriceSimilarites(dataset)
    print(mat)
    print(mat[:,1:].sum())

    stageComputeMatrix_time = datetime.now()
    print('Calcul de toutes les similarités : ', stageComputeMatrix_time - start_time, ' (hh:mm:ss.ms)')

    newDF = pd.DataFrame(mat[:,1:], index=mat[:,0], columns=list(dataset['Entry']))
    print(newDF)

    stageDataframeCreation_time = datetime.now()
    print('Création du dataframe : ', stageDataframeCreation_time - start_time, ' (hh:mm:ss.ms)')

    newDF.to_csv(path_or_buf=output_matrix_path)

    stageCSVExport_time = datetime.now()
    print('Création du dataset : ', stageDSCreated_time - start_time, ' (hh:mm:ss.ms)')
    print('Calcul de toutes les similarités : ', stageComputeMatrix_time - start_time, ' (hh:mm:ss.ms)')
    print('Création du dataframe : ', stageDataframeCreation_time - start_time, ' (hh:mm:ss.ms)')
    print('Temps d\'exécution total :', stageCSVExport_time - start_time)
