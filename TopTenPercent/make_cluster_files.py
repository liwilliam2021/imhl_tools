import pandas as pd
import time
pd.options.mode.chained_assignment = None

NUM_CLUSTERS = 461
BASE_PATH = 'TopTenPercent/baseline.tsv'

def make_pvalue_files (disorder="SCZ_2022"):
    print ("Loading excel...")
    xls = pd.ExcelFile("TopTenPercent/MAGMA_Gene_Level_Analysis_Results_03_03_23_Modified.xlsx")
    df = pd.read_excel(xls, disorder)

    print ("Loading other disorders...")
    s2018_file = 'TopTenPercent/disorders/clozuk_pgc2.meta.sumstats.txt_step2.genes.out'
    s2014_file = 'TopTenPercent/disorders/final_daner_natgen_pgc_eur_step2.genes.out'
    s2011_file = 'TopTenPercent/disorders/BPSCZ.scz-only.results.txt_step2.genes.out'
    alc_file = 'TopTenPercent/disorders/DRNKWK_CUT_SUMSTATS_step2.genes.out'
    ms_file = 'TopTenPercent/disorders/discovery_metav3.0.meta.step2.genes.out'
    alz_file = 'TopTenPercent/disorders/ALZHEIMER_SUMSTATS.txt_step2.genes.out'
    sleep_file = 'TopTenPercent/disorders/sleepdurationsumstats.txt_step2.genes.out'
    ptsd_file = 'TopTenPercent/disorders/eur_ptsd_pcs_v4_aug3_2021.allchrX.fuma_step2.genes (1).out'
    bmi_file = 'TopTenPercent/disorders/Meta-analysis_Locke_et_al+UKBiobank_2018_UPDATED.txt_step2.genes.out'
    cig_file = 'TopTenPercent/disorders/CIGDAY_CUT_SUMSTATS_step2.genes.out'
    mdd2023_file = 'TopTenPercent/disorders/MDD_2023_SUMSTATS.txt_step2.genes.out'
    mdd2019_file = 'TopTenPercent/disorders/2019-pgc-ukb-depression-genome-wide_final.txt_step2.genes (1).out'

    adhd_file = 'TopTenPercent/disorders/daner_adhd_meta_filtered_NA_iPSYCH23_PGC11_sigPCs_woSEX_2ell6sd_EUR_Neff_70.meta_step2.genes.out'
    an_file = 'TopTenPercent/disorders/final_pgcAN2.2019-07-cleaned.vcf.tsv.txt_step2.genes (1).out'
    asd_file = 'TopTenPercent/disorders/iPSYCH-PGC_ASD_Nov2017_step2.genes.out'
    bip_file = 'TopTenPercent/disorders/pgc-bip2021-all.vcf.tsv_step2.genes.out'
    educ_file = 'TopTenPercent/disorders/GWAS_EA_excl23andMe.txtdl=0_step2.genes.out'
    hgt_file = 'TopTenPercent/disorders/Meta-analysis_Wood_et_al+UKBiobank_2018.txt_step2.genes.out'
    intel_file = 'TopTenPercent/disorders/SavageJansen_2018_intelligence_metaanalysis.txt_step2.genes.out'
    neuro_file = 'TopTenPercent/disorders/sumstats_neuroticism_ctg_format_oneSNPcol.txt_step2.genes.out'

    s2018 = pd.read_csv(s2018_file, sep=r"\s+")[["GENE", "P"]]
    s2018_genes = set(s2018['GENE'])
    s2014 = pd.read_csv(s2014_file, sep=r"\s+")[["GENE", "P"]]
    s2014_genes = set(s2014['GENE'])
    s2011 = pd.read_csv(s2011_file, sep=r"\s+")[["GENE", "P"]]
    s2011_genes = set(s2011['GENE'])

    alc = pd.read_csv(alc_file, sep=r"\s+")[["GENE", "P"]]
    alc_genes = set(alc['GENE'])
    ms = pd.read_csv(ms_file, sep=r"\s+")[["GENE", "P"]]
    ms_genes = set(ms['GENE'])
    sleep = pd.read_csv(sleep_file, sep=r"\s+")[["GENE", "P"]]
    sleep_genes = set(sleep['GENE'])
    alz = pd.read_csv(alz_file, sep=r"\s+")[["GENE", "P"]]
    alz_genes = set(alz['GENE'])
    ptsd = pd.read_csv(ptsd_file, sep=r"\s+")[["GENE", "P"]]
    ptsd_genes = set(ptsd['GENE'])
    bmi = pd.read_csv(bmi_file, sep=r"\s+")[["GENE", "P"]]
    bmi_genes = set(bmi['GENE'])
    cig = pd.read_csv(cig_file, sep=r"\s+")[["GENE", "P"]]
    cig_genes = set(cig['GENE'])
    mdd2023 = pd.read_csv(mdd2023_file, sep=r"\s+")[["GENE", "P"]]
    mdd2023_genes = set(mdd2023['GENE'])
    mdd2019 = pd.read_csv(mdd2019_file, sep=r"\s+")[["GENE", "P"]]
    mdd2019_genes = set(mdd2019['GENE'])

    adhd = pd.read_csv(adhd_file, sep=r"\s+")[["GENE", "P"]]
    adhd_genes = set(adhd['GENE'])
    an = pd.read_csv(an_file, sep=r"\s+")[["GENE", "P"]]
    an_genes = set(an['GENE'])
    asd = pd.read_csv(asd_file, sep=r"\s+")[["GENE", "P"]]
    asd_genes = set(asd['GENE'])
    bip = pd.read_csv(bip_file, sep=r"\s+")[["GENE", "P"]]
    bip_genes = set(bip['GENE'])
    educ = pd.read_csv(educ_file, sep=r"\s+")[["GENE", "P"]]
    educ_genes = set(educ['GENE'])
    hgt = pd.read_csv(hgt_file, sep=r"\s+")[["GENE", "P"]]
    hgt_genes = set(hgt['GENE'])
    intel = pd.read_csv(intel_file, sep=r"\s+")[["GENE", "P"]]
    intel_genes = set(intel['GENE'])
    neuro = pd.read_csv(neuro_file, sep=r"\s+")[["GENE", "P"]]
    neuro_genes = set(neuro['GENE'])

    print ("Editing base file...")
    df.rename(columns={'P': 'SCZ.2022.P'}, inplace=True)
    df["SCZ.2018.P"] = [s2018.at[s2018.loc[s2018['GENE'] == gnum].index.to_numpy()[0], "P"] if gnum in s2018_genes else '' for gnum in df["GENE"]]
    df["SCZ.2014.P"] = [s2014.at[s2014.loc[s2014['GENE'] == gnum].index.to_numpy()[0], "P"] if gnum in s2014_genes else '' for gnum in df["GENE"]]
    df["SCZ.2011.P"] = [s2011.at[s2011.loc[s2011['GENE'] == gnum].index.to_numpy()[0], "P"] if gnum in s2011_genes else '' for gnum in df["GENE"]]
    df["alcohol.2022.P"] = [alc.at[alc.loc[alc['GENE'] == gnum].index.to_numpy()[0], "P"] if gnum in alc_genes else '' for gnum in df["GENE"]]
    df["MS.2018.P"] = [ms.at[ms.loc[ms['GENE'] == gnum].index.to_numpy()[0], "P"] if gnum in ms_genes else '' for gnum in df["GENE"]]
    df["sleep.2019.P"] = [sleep.at[sleep.loc[sleep['GENE'] == gnum].index.to_numpy()[0], "P"] if gnum in sleep_genes else '' for gnum in df["GENE"]]
    df["ALZ.2022.P"] = [alz.at[alz.loc[alz['GENE'] == gnum].index.to_numpy()[0], "P"] if gnum in alz_genes else '' for gnum in df["GENE"]]
    df["PTSD.2023.P"] = [ptsd.at[ptsd.loc[ptsd['GENE'] == gnum].index.to_numpy()[0], "P"] if gnum in ptsd_genes else '' for gnum in df["GENE"]]
    df["BMI.2018.P"] = [bmi.at[bmi.loc[bmi['GENE'] == gnum].index.to_numpy()[0], "P"] if gnum in bmi_genes else '' for gnum in df["GENE"]]
    df["CIG.2022.P"] = [cig.at[cig.loc[cig['GENE'] == gnum].index.to_numpy()[0], "P"] if gnum in cig_genes else '' for gnum in df["GENE"]]
    df["MDD.2023.P"] = [mdd2023.at[mdd2023.loc[mdd2023['GENE'] == gnum].index.to_numpy()[0], "P"] if gnum in mdd2023_genes else '' for gnum in df["GENE"]]
    df["MDD.2019.P"] = [mdd2019.at[mdd2019.loc[mdd2019['GENE'] == gnum].index.to_numpy()[0], "P"] if gnum in mdd2019_genes else '' for gnum in df["GENE"]]
    df["ADHD.2019.P"] = [adhd.at[adhd.loc[adhd['GENE'] == gnum].index.to_numpy()[0], "P"] if gnum in adhd_genes else '' for gnum in df["GENE"]]
    df["AN.2019.P"] = [an.at[an.loc[an['GENE'] == gnum].index.to_numpy()[0], "P"] if gnum in an_genes else '' for gnum in df["GENE"]]
    df["ASD.2017.P"] = [asd.at[asd.loc[asd['GENE'] == gnum].index.to_numpy()[0], "P"] if gnum in asd_genes else '' for gnum in df["GENE"]]
    df["BIP.2021.P"] = [bip.at[bip.loc[bip['GENE'] == gnum].index.to_numpy()[0], "P"] if gnum in bip_genes else '' for gnum in df["GENE"]]
    df["EDUC.2018.P"] = [educ.at[educ.loc[educ['GENE'] == gnum].index.to_numpy()[0], "P"] if gnum in educ_genes else '' for gnum in df["GENE"]]
    df["HGT.2018.P"] = [hgt.at[hgt.loc[hgt['GENE'] == gnum].index.to_numpy()[0], "P"] if gnum in hgt_genes else '' for gnum in df["GENE"]]
    df["INTEL.2018.P"] = [intel.at[intel.loc[intel['GENE'] == gnum].index.to_numpy()[0], "P"] if gnum in intel_genes else '' for gnum in df["GENE"]]
    df["NEURO.2018.P"] = [neuro.at[neuro.loc[neuro['GENE'] == gnum].index.to_numpy()[0], "P"] if gnum in neuro_genes else '' for gnum in df["GENE"]]

    df.to_csv(BASE_PATH, sep="\t", index=False)
    print ("Base file saved...")


# Makes a file for each cluster
def make_all_files ():
    
    print ("Loading base file...")
    new_df = pd.read_csv(BASE_PATH, sep='\t')

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

    spec_genes = set (cont_spec_df['GENE'])
    ECAH_genes = set (ECAH_spec_df['GENE'])
    neuron_genes = set (neuron_spec_df['GENE'])
    inter_genes = set (inter_spec_df['GENE'])

    print ("Making Cluster Files")
    start_time = time.time()

    for i in range(240, NUM_CLUSTERS):
        name = f'Cluster{i}'
        # new_df = df.loc[df['GENE'].isin(genes_by_cluster[name])]
        new_df["SPE_RANK"] = [genes_by_cluster[name].index(gnum) + 1 if gnum in genes_by_cluster[name] else '' for gnum in new_df["GENE"]]
        new_df.sort_values("SCZ.2022.P", ascending=True, inplace=True)
        new_df["SPE_VAL"] = [cont_spec_df.at[cont_spec_df.loc[cont_spec_df['GENE'] == gnum].index.to_numpy()[0], name] if gnum in spec_genes else '' for gnum in new_df["GENE"]]
        if name in ECAH_spec_df.columns:
          new_df["SPE_EXCITE"] = [ECAH_spec_df.at[ECAH_spec_df.loc[ECAH_spec_df['GENE'] == gnum].index.to_numpy()[0], name] if gnum in ECAH_genes else '' for gnum in new_df["GENE"]]
        if name in neuron_spec_df.columns:
          new_df["SPE_NEURON"] = [neuron_spec_df.at[neuron_spec_df.loc[neuron_spec_df['GENE'] == gnum].index.to_numpy()[0], name] if gnum in neuron_genes else '' for gnum in new_df["GENE"]]
        if name in inter_spec_df.columns:
          new_df["SPE_INTER"] = [inter_spec_df.at[inter_spec_df.loc[inter_spec_df['GENE'] == gnum].index.to_numpy()[0], name] if gnum in inter_genes else '' for gnum in new_df["GENE"]]
        new_df["GENE_EXP"] = [express_df.at[express_df.loc[express_df['GENE'] == gnum].index.to_numpy()[0], name] if gnum in inter_genes else '' for gnum in new_df["GENE"]]

        out_folder = "CompositeClusterFiles"
        new_df.to_csv(f'TopTenPercent/{out_folder}/Cluster_{i}.tsv', sep="\t", index=False)

        if i % 10 == 0:
          elapsed_time = time.time() - start_time
          print (f"Cluster {i}, estimated time left: {elapsed_time * (NUM_CLUSTERS - i - 1) / (i + 1) }")
    print ("Done.")

if __name__ == "__main__":
    # make_pvalue_files ()
    make_all_files ()