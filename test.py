import pandas as pd

df = pd.read_excel("MAGMA_Gene_Level_Analysis_Results_03_03_23.xlsx", "SCZ_2022")

scz_genes = set(df['GENE'])

df2 = pd.read_csv("TopTenPercent/CompositeClusterFiles/Cluster_6.tsv", sep='\t')

genes2 = set(df2['GENE'])

print (len(scz_genes) - len(genes2))

print (794 in scz_genes)

print (794 in genes2)