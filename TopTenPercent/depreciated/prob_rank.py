import pandas as pd
pd.options.mode.chained_assignment = None

#NOTE: FILE DEPRECIATED-- use MAKE_CLUSTER_FILES

NUM_CLUSTERS = 461

# Takes the top 10% most specific genes for each cluster and ranks them by
# p-value for the given disorder. Makes a file for each cluster
def make_pvalue_files (disorder="SCZ_2022", top_ten = False):
    
    print ("Getting genes from Siletti clusters...")
    specificity_file = "TopTenPercent/Siletti_Cluster_top10.txt" if top_ten else "TopTenPercent/genes-desc-ordered-by-spe_from-spe-matrix.txt"
    with open(specificity_file, 'r') as f:
        clusters = list(map(lambda text: text.strip('\n').split("	"), f.readlines()))
        assert(len(clusters) == NUM_CLUSTERS)
        genes_by_cluster = {clusters[i][0]: [int(num) for num in clusters[i][1:]] for i in range(NUM_CLUSTERS)}
    print ("Loaded.")

    # total_set = set()
    # for i in range(NUM_CLUSTERS):
    #     total_set = total_set.union(set(genes_by_cluster[f'Cluster{i}']))
    # print (len(total_set))

    print ("Loading excel...")
    df = pd.read_excel("TopTenPercent/MAGMA_Gene_Level_Analysis_Results_03_03_23_Modified.xlsx", disorder)
    print ("Loaded.")

    without_pvalues = set()

    for i in range(NUM_CLUSTERS):
        new_df = df.loc[df['GENE'].isin(genes_by_cluster[f'Cluster{i}'])]
        new_df.sort_values("P", ascending=True)
        new_df["SPERANK"] = [genes_by_cluster[f'Cluster{i}'].index(gnum) + 1 for gnum in new_df["GENE"]]
        # extra1 = [j for j in genes_by_cluster[f'Cluster{i}'] if j not in list(new_df['GENE'])]
        # extra2 = [j for j in list(new_df['GENE']) if j not in genes_by_cluster[f'Cluster{i}']]
        # without_pvalues = without_pvalues.union(set(extra1))

        # print (f'Cluster{i} missing {len (extra1)} p-values')

        # assert (len(extra2) == 0)
        # assert (len(new_df.index) == len(genes_by_cluster[f'Cluster{i}']) - len(extra1))
        # assert(new_df.shape[0] -1  == len(genes_by_cluster[f'Cluster{i}']))
        out_folder = "TopClusterFiles" if top_ten else "AllClusterFiles" 
        # Remove 10% name
        new_df.to_csv(f'TopTenPercent/{out_folder}/Cluster_{i}_{disorder}_siletti10percent.tsv', sep="\t", index=False)
        print (f"Cluster {i} has {len(new_df.index)}")
        # print (new_df)
    print ("Done.")

    # print (f'The following {len(without_pvalues)} gene numbers did not have p-values')
    # print (without_pvalues)

def get_gene_spe_rank (disorder="SCZ_2022", gene_num = 1813):
    rank_info = pd.DataFrame(columns=['CLUSTER', 'TOP_DECILE', 'RANK'])
    for i in range(NUM_CLUSTERS):
        df1 = pd.read_csv(f'TopTenPercent/TopClusterFiles/Cluster_{i}_{disorder}_siletti10percent.tsv', sep='\t')
        df2 = pd.read_csv(f'TopTenPercent/AllClusterFiles/Cluster_{i}_{disorder}_siletti10percent.tsv', sep='\t')
        data = pd.DataFrame([{'CLUSTER': i, 'TOP_DECILE': gene_num in df1['GENE'].values, 'RANK': df2.loc[df2["GENE"] == gene_num, "SPERANK"].values[0]}])
        rank_info = pd.concat([rank_info, data], ignore_index=True)
    print (rank_info)
    rank_info.to_csv(f'TopTenPercent/gene_num{gene_num}_{disorder}_siletti10percent.tsv', sep="\t", index=False)



if __name__ == "__main__":
    make_pvalue_files ()
    # get_gene_spe_rank ()