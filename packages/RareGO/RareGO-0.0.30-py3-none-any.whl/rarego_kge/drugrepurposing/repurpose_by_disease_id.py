# -*- coding: utf-8 -*-

import pandas as pd
import torch
from pykeen import predict

class DiseaseDrugRepurposer:
    def __init__(self, model_path, model2_path, default_disease_id=['D010051'], default_relation="DRUG_DISEASE_ASSOCIATION"):
        """
        Initialize the DiseaseDrugRepurposer class.

        Parameters:
        - model_path (str): Path to the pre-trained embedding model.
        - model2_path (str): Path to the pre-trained knowledge graph model training data.
        - default_disease_id (list of str): Default disease IDs to use if not specified later.
        - default_relation (str): Default relation to use if not specified later.
        """
        self.model = torch.load(model_path)
        self.model2 = torch.load(model2_path)
        self.default_disease_id = default_disease_id
        self.default_relation = default_relation

    def repurpose_by_disease_id(self, disease_id=None, relation=None):
        """
        Repurpose drugs for given disease IDs.

        Parameters:
        - disease_id (list of str, optional): List of disease IDs for which drug repurposing is to be performed.
        - relation (str, optional): The relation type between drugs and diseases in the knowledge graph.

        Returns:
        - pandas.DataFrame: A DataFrame containing predicted drug-disease associations for the given disease IDs.
        """
        disease_id = disease_id or self.default_disease_id
        relation = relation or self.default_relation

        disease_drug = []
        for tid in disease_id:
            drugs = predict.predict_target(model=self.model, tail=tid, relation=relation, triples_factory=self.model2).df 
            disease_drug.append(drugs)
        return pd.concat(disease_drug)

    def main(self, disease_id=None, relation=None, output_file='example2.tsv'):
        """
        Main method to repurpose drugs and save results.

        Parameters:
        - disease_id (list of str, optional): List of disease IDs for which drug repurposing is to be performed.
        - relation (str, optional): The relation type between drugs and diseases in the knowledge graph.
        - output_file (str): The name of the output file to save results.
        """
        # Repurpose drugs for given disease IDs
        disease_drug = self.repurpose_by_disease_id(disease_id, relation)
        print(disease_drug)
        # Save results to CSV
        disease_drug.to_csv(output_file, index=False, sep='\t')

# Example usage
if __name__ == "__main__":
    model_path = 'C:/Users/bpatton23/Downloads/Drugrepurposing (1)/Drugrepurposing/complex_model_gene/trained_model.pkl'
    model2_path = 'C:/Users/bpatton23/Downloads/Drugrepurposing (1)/Drugrepurposing/complex_model_gene/complex_training5'

    # Initialize with default values
    repurposer = DiseaseDrugRepurposer(model_path, model2_path)

    # Use default values
    repurposer.main()

    # Specify custom disease IDs and relation
    custom_disease_ids = ['D003924', 'D005128']
    custom_relation = "CUSTOM_RELATION"
    repurposer.main(disease_id=custom_disease_ids, relation=custom_relation, output_file='custom_output.tsv')

    # You can also create an instance with different defaults
    repurposer2 = DiseaseDrugRepurposer(model_path, model2_path, 
                                        default_disease_id=['D005128'], 
                                        default_relation="ANOTHER_RELATION")
    repurposer2.main()  # This will use the new defaults
