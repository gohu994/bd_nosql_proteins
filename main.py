import pandas as pd 

brut = pd.read_csv(r'datas/test.tab', sep='\t')
domains = brut["Cross-reference (InterPro)"].str.split(';')
dataset = pd.DataFrame({'Entry': brut["Entry"], 'Domains': domains[:]})

print(dataset)
