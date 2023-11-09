import numpy as np
import pandas as pd
import loompy

filepath = "./adult_human_20221007.agg.loom"

enrichment_df = pd.DataFrame()

out_folder = "CompositeClusterFiles"
genes_df = pd.read_csv(f'../TopTenPercent/{out_folder}/Cluster_{0}.tsv', sep="\t")
stored_genes = set(genes_df['Name'])
genes_to_convert = set ()

with loompy.connect(filepath) as ds:
  genes = ds.ra.Gene
  for gene in stored_genes:
      if gene not in genes: genes_to_convert.add (gene)

  for (ix, selection, view) in ds.scan(axis=0):
    enrichment_data = view['enrichment']
    print (genes [selection])
    break
    print (ix)
    print (enrichment_data.shape)
    print (view.shape)
    print (max(selection))

print (genes_to_convert)