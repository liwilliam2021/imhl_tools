import pandas as pd
pd.options.mode.chained_assignment = None

NUM_CLUSTERS = 461

# Makes a file for each cluster
def make_pvalue_files (disorder="SCZ_2022"):
    
    print ("Getting genes from Siletti clusters...")
    gene_specificity_file = "TopTenPercent/genes-desc-ordered-by-spe_from-spe-matrix.txt"
    with open(gene_specificity_file, 'r') as f:
        clusters = list(map(lambda text: text.strip('\n').split("	"), f.readlines()))
        assert(len(clusters) == NUM_CLUSTERS)
        genes_by_cluster = {clusters[i][0]: [int(num) for num in clusters[i][1:]] for i in range(NUM_CLUSTERS)}

    print ("Getting specificity TSVs...")
    expression_file = "TopTenPercent/proportion_cells_expressing_genes_matrix.txt"
    cont_spec_file = "TopTenPercent/conti_specificity_matrix.txt"
    ECAH_spec_file = "TopTenPercent/conti_specificity_matrix_cluster83-205_excitatory-cortical-amygdala-hippocampal.txt"
    neuron_spec_file = "TopTenPercent/conti_specificity_matrix_cluster83-460_neurons.txt"
    inter_spec_file = "TopTenPercent/conti_specificity_matrix_cluster239-296_interneurons.txt"

    express_df = pd.read_csv(expression_file, sep='\t')
    cont_spec_df = pd.read_csv(cont_spec_file , sep='\t')
    ECAH_spec_df = pd.read_csv(ECAH_spec_file , sep='\t')
    neuron_spec_df = pd.read_csv(neuron_spec_file , sep='\t')
    inter_spec_df = pd.read_csv(inter_spec_file , sep='\t')
    print ("Done.")

    ECAH_genes = set (ECAH_spec_df['GENE'])
    neuron_genes = set (neuron_spec_df['GENE'])
    inter_genes = set (inter_spec_df['GENE'])

    print ("Loading excel...")
    xls = pd.ExcelFile("TopTenPercent/MAGMA_Gene_Level_Analysis_Results_03_03_23_Modified.xlsx")
    df = pd.read_excel(xls, disorder)

    print ("Loading other disorders...")
    alc = pd.read_excel(xls, "DRNKWK")[["GENE", "P"]]
    alc_genes = set(alc['GENE'])
    sleep = pd.read_excel(xls, "SLEEP_DURATION")[["GENE", "P"]]
    sleep_genes = set(sleep['GENE'])
    bmi = pd.read_excel(xls, "BMI")[["GENE", "P"]]
    bmi_genes = set(bmi['GENE'])
    cig = pd.read_excel(xls, "CIGDAY")[["GENE", "P"]]
    cig_genes = set(cig['GENE'])
    mdd = pd.read_excel(xls, "MDD")[["GENE", "P"]]
    mdd_genes = set(mdd['GENE'])
    s2018 = pd.read_excel(xls, "SCZ_2018")[["GENE", "P"]]
    s2018_genes = set(s2018['GENE'])
    s2014 = pd.read_excel(xls, "SCZ_2014")[["GENE", "P"]]
    s2014_genes = set(s2014['GENE'])
    s2011 = pd.read_excel(xls, "SCZ_2011")[["GENE", "P"]]
    s2011_genes = set(s2011['GENE'])
    print ("Loaded.")

    for i in range(NUM_CLUSTERS):
        name = f'Cluster{i}'
        new_df = df.loc[df['GENE'].isin(genes_by_cluster[name])]
        new_df.rename(columns={'P': 'SCZ.2022.P'}, inplace=True)
        new_df["alcohol.2022.P"] = [alc.at[alc.loc[alc['GENE'] == gnum].index.to_numpy()[0], "P"] if gnum in alc_genes else '' for gnum in new_df["GENE"]]
        new_df["sleep.2019.P"] = [sleep.at[sleep.loc[sleep['GENE'] == gnum].index.to_numpy()[0], "P"] if gnum in sleep_genes else '' for gnum in new_df["GENE"]]
        new_df["BMI.2018.P"] = [bmi.at[bmi.loc[bmi['GENE'] == gnum].index.to_numpy()[0], "P"] if gnum in bmi_genes else '' for gnum in new_df["GENE"]]
        new_df["CIG.2022.P"] = [cig.at[cig.loc[cig['GENE'] == gnum].index.to_numpy()[0], "P"] if gnum in cig_genes else '' for gnum in new_df["GENE"]]
        new_df["MDD.2019.P"] = [mdd.at[mdd.loc[mdd['GENE'] == gnum].index.to_numpy()[0], "P"] if gnum in mdd_genes else '' for gnum in new_df["GENE"]]
        new_df["SCZ.2018.P"] = [s2018.at[s2018.loc[s2018['GENE'] == gnum].index.to_numpy()[0], "P"] if gnum in s2018_genes else '' for gnum in new_df["GENE"]]
        new_df["SCZ.2014.P"] = [s2014.at[s2014.loc[s2014['GENE'] == gnum].index.to_numpy()[0], "P"] if gnum in s2014_genes else '' for gnum in new_df["GENE"]]
        new_df["SCZ.2011.P"] = [s2011.at[s2011.loc[s2011['GENE'] == gnum].index.to_numpy()[0], "P"] if gnum in s2011_genes else '' for gnum in new_df["GENE"]]
        new_df["SPE_RANK"] = [genes_by_cluster[name].index(gnum) + 1 for gnum in new_df["GENE"]]
        new_df.sort_values("SCZ.2022.P", ascending=True, inplace=True)
        new_df["SPE_VAL"] = [cont_spec_df.at[cont_spec_df.loc[cont_spec_df['GENE'] == gnum].index.to_numpy()[0], name] for gnum in new_df["GENE"]]
        if name in ECAH_spec_df.columns:
          new_df["SPE_EXCITE"] = [ECAH_spec_df.at[ECAH_spec_df.loc[ECAH_spec_df['GENE'] == gnum].index.to_numpy()[0], name] if gnum in ECAH_genes else '' for gnum in new_df["GENE"]]
        if name in neuron_spec_df.columns:
          new_df["SPE_NEURON"] = [neuron_spec_df.at[neuron_spec_df.loc[neuron_spec_df['GENE'] == gnum].index.to_numpy()[0], name] if gnum in neuron_genes else '' for gnum in new_df["GENE"]]
        if name in inter_spec_df.columns:
          new_df["SPE_INTER"] = [inter_spec_df.at[inter_spec_df.loc[inter_spec_df['GENE'] == gnum].index.to_numpy()[0], name] if gnum in inter_genes else '' for gnum in new_df["GENE"]]
        new_df["GENE_EXP"] = [express_df.at[express_df.loc[express_df['GENE'] == gnum].index.to_numpy()[0], name] for gnum in new_df["GENE"]]

        out_folder = "CompositeClusterFiles"
        new_df.to_csv(f'TopTenPercent/{out_folder}/Cluster_{i}.tsv', sep="\t", index=False)
        print (f"Cluster {i} has {len(new_df.index)}")
    print ("Done.")

if __name__ == "__main__":
    make_pvalue_files ()