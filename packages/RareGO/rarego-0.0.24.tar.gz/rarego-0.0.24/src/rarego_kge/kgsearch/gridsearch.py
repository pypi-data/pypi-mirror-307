# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 13:49:18 2024

@author: bpatton23
"""
from pykeen.losses import MarginRankingLoss
from pykeen.losses import BCEWithLogitsLoss, NSSALoss, SoftplusLoss
from pykeen.evaluation import RankBasedEvaluator
from optuna.samplers import GridSampler
from pykeen.sampling import NegativeSampler
from pykeen.datasets import Nations
from pykeen.models import TransE,DistMult,TransH,HolE,RotatE,KG2E

import torch
from pykeen.hpo import hpo_pipeline
from optuna.samplers import GridSampler
from pykeen.stoppers import EarlyStopper
from pykeen.datasets import PathDataset
from sklearn.model_selection import train_test_split
import random

Model_Zoo=['autosf', 'complex', 'crosse', 'mure', 'proje', 'quate']

custom_dataset = PathDataset.from_path('C:/Users/bpatton23/Downloads/Drugrepurposing/R25KG-Rare.tsv')
custom_dataset
def grid_search(n_trials=30,search_space=None, dataset=custom_dataset, model_name='autosf'):
    if search_space is None:
        search_space = {
            "model.embedding_dim": [208, 224, 240,256],
            "model.scoring_fct_norm": [1, 2],
            "loss.margin": [0.1],
            "optimizer.lr": [0.001],
            "negative_sampler.num_negs_per_pos": [1,5,10,20],
            "training.num_epochs": [200,300],
            "training.batch_size": [1024],
            "loss": ["bcewithlogits","SoftplusLoss"],
            "negative_sampler": ["basic","BernoulliNegativeSampler"],
            "optimizer": ["SGD","Adam"],
            "training_loop": ["sLCWA","sLCWANegativeSampling"],
        }
    hpo_pipeline_result = hpo_pipeline(
        n_trials=n_trials,
        sampler=GridSampler,
        sampler_kwargs=dict(search_space=search_space),
        dataset=dataset,
        model=model_name,
        stopper='early',
        stopper_kwargs=dict(frequency=100, patience=110, relative_delta=0.02, metric="mean_reciprocal_rank", larger_is_better=True)
    )
    return hpo_pipeline_result.save_to_directory('autosf_grid_search')
    #Hyper = torch.load('C:/Users/bpatton23/Downloads/Drugrepurposing/proje_hyperparam')
    #print(Hyper)
    #torch.save(ev.training, 'rgcn_training')

# Example usage
best_hyperparameters = grid_search()
torch.save(best_hyperparameters, 'autosf_hyperparam')
#best_hyperparameters.save_to_directory('proje_grid_search')
print(best_hyperparameters)
