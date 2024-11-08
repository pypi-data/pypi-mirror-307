# -*- coding: utf-8 -*-
"""
Created on Thu May  9 21:52:31 2024

@author: bpatton23
"""
import pandas as pd
import torch
from pykeen import predict

class GeneFunctionRepurposer:
    def __init__(self, model_path, model2_path, default_targets=['Q14865']):
        """
        Initialize the GeneFunctionRepurposer class.

        Parameters:
        - model_path (str): Path to the pre-trained embedding model.
        - model2_path (str): Path to the pre-trained knowledge graph model training data.
        - default_targets (list of str): Default protein IDs to use if not specified later.
        """
        self.model = torch.load(model_path)
        self.model2 = torch.load(model2_path)
        self.default_targets = default_targets

    def repurpose_by_gene_ids(self, targets=None, relation="GO_MF"):
        """
        Repurpose GeneID for given protein ID.

        Parameters:
        - targets (list of str, optional): Protein IDs for which protein function prediction is to be performed.
        - relation (str): The relation type between protein and gene ontology terms in the knowledge graph.

        Returns:
        - pandas.DataFrame: A DataFrame containing predicted functions for the given protein IDs.
        """
        targets = targets or self.default_targets
        drug_list = []
        for hid in targets:
            drugs = predict.predict_target(model=self.model, head=hid, relation=relation, triples_factory=self.model2).df 
            drug_list.append(drugs)
        return pd.concat(drug_list)

    def main(self, targets=None, output_prefix='Gene_ID'):
        """
        Main method to predict gene functions and save results.

        Parameters:
        - targets (list of str, optional): Protein IDs for which protein function prediction is to be performed.
        - output_prefix (str): Prefix for output file names.
        """
        targets = targets or self.default_targets

        # Predict GeneID for given protein ID
        gene_mf = self.repurpose_by_gene_ids(targets, relation="GO_MF")
        gene_bp = self.repurpose_by_gene_ids(targets, relation="GO_BP")
        gene_cc = self.repurpose_by_gene_ids(targets, relation="GO_CC")

        print("Molecular Function predictions:")
        print(gene_mf)
        print("\nBiological Process predictions:")
        print(gene_bp)
        print("\nCellular Component predictions:")
        print(gene_cc)

        # Save results to CSV
        gene_mf.to_csv(f'{output_prefix}_MF.tsv', index=False, sep='\t')
        gene_bp.to_csv(f'{output_prefix}_BP.tsv', index=False, sep='\t')
        gene_cc.to_csv(f'{output_prefix}_CC.tsv', index=False, sep='\t')

# Example usage
if __name__ == "__main__":
    model_path = 'C:/Users/bpatton23/Downloads/Drugrepurposing/complex_model_gene/trained_model.pkl'
    model2_path = 'C:/Users/bpatton23/Downloads/Drugrepurposing/complex_model_gene/complex_training5'

    # Initialize with default values
    repurposer = GeneFunctionRepurposer(model_path, model2_path)

    # Use default values
    repurposer.main()

    # Specify custom protein IDs
    custom_targets = ['P12345', 'Q67890']
    repurposer.main(targets=custom_targets, output_prefix='Custom_Gene_ID')

    # You can also create an instance with different defaults
    repurposer2 = GeneFunctionRepurposer(model_path, model2_path, default_targets=['P98765'])
    repurposer2.main()  # This will use the new defaults








