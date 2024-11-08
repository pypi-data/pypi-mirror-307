# -*- coding: utf-8 -*-
"""
Created on Thu May  9 22:05:21 2024

@author: bpatton23
"""
import torch
from pykeen import predict
import pandas as pd

class DrugRepurposer:
    def __init__(self, model_path, model2_path, default_drugs=['DB09052', 'DB05889', 'DB13881', 'DB08870', 'DB08901'], default_relation="DRUG_DISEASE_ASSOCIATION"):
        """
        Initialize the DrugRepurposer class.

        Parameters:
        - model_path (str): Path to the pre-trained embedding model.
        - model2_path (str): Path to the pre-trained knowledge graph model training data.
        - default_drugs (list of str): Default drug IDs to use if not specified later.
        - default_relation (str): Default relation to use if not specified later.
        """
        self.model = torch.load(model_path)
        self.model2 = torch.load(model2_path)
        self.default_drugs = default_drugs
        self.default_relation = default_relation

    def repurpose_by_drug_ids(self, drugs=None, relation=None):
        """
        Repurpose drugs for given drug IDs.

        Parameters:
        - drugs (list of str, optional): List of drug IDs for which drug repurposing is to be performed.
        - relation (str, optional): The relation type between drugs and diseases in the knowledge graph.

        Returns:
        - pandas.DataFrame: A DataFrame containing predicted drug-disease associations for the given drug IDs.
        """
        drugs = drugs or self.default_drugs
        relation = relation or self.default_relation

        drug_disease = []
        for hid in drugs:
            diseases = predict.predict_target(model=self.model, head=hid, relation=relation, triples_factory=self.model2).df 
            drug_disease.append(diseases)
        return pd.concat(drug_disease)

    def main(self, drugs=None, relation=None, output_file='example.tsv'):
        """
        Main method to repurpose drugs and save results.

        Parameters:
        - drugs (list of str, optional): List of drug IDs for which drug repurposing is to be performed.
        - relation (str, optional): The relation type between drugs and diseases in the knowledge graph.
        - output_file (str): The name of the output file to save results.
        """
        # Repurpose drugs for given drug IDs
        drug_disease = self.repurpose_by_drug_ids(drugs, relation)
        print(drug_disease)
        # Save results to CSV
        drug_disease.to_csv(output_file, index=False, sep='\t')

# Example usage
if __name__ == "__main__":
    model_path = 'C:/Users/bpatton23/Downloads/Drugrepurposing (1)/Drugrepurposing/complex_model_gene/trained_model.pkl'
    model2_path = 'C:/Users/bpatton23/Downloads/Drugrepurposing (1)/Drugrepurposing/complex_model_gene/complex_training5'

    # Initialize with default values
    repurposer = DrugRepurposer(model_path, model2_path)

    # Use default values
    repurposer.main()

    # Specify custom drug IDs and relation
    custom_drugs = ['DB00001', 'DB00002', 'DB00003']
    custom_relation = "CUSTOM_RELATION"
    repurposer.main(drugs=custom_drugs, relation=custom_relation, output_file='custom_output.tsv')

    # You can also create an instance with different defaults
    repurposer2 = DrugRepurposer(model_path, model2_path, 
                                 default_drugs=['DB00004', 'DB00005'], 
                                 default_relation="ANOTHER_RELATION")
    repurposer2.main()  # This will use the new defaults