# -*- coding: utf-8 -*-
"""
Created on Tue May 14 15:21:22 2024

@author: bpatton23
"""

import numpy as np
import pandas as pd
from pickle import dump, load

import torch
import torch.optim as optim
import pykeen
from pykeen.pipeline import pipeline
from pykeen.pipeline import plot
from pykeen import predict
from pykeen.hpo import hpo_pipeline
from pykeen.losses import MarginRankingLoss
from pykeen.losses import BCEWithLogitsLoss, NSSALoss, SoftplusLoss
from pykeen.evaluation import RankBasedEvaluator
from optuna.samplers import GridSampler
from pykeen.sampling import NegativeSampler
from pykeen.datasets import Nations
from pykeen.models import TransE,DistMult,TransH,HolE,RotatE,KG2E

from .kgIO import train_test_val_split_from_csv 

from pickle import load, dump 
from pykeen.triples import TriplesFactory

Model_Zoo=['autosf', 'boxe', 'compgcn', 'complex', 'complexliteral', 'conve',
           'convkb', 'cooccurrencefiltered', 'cp', 'crosse', 'distma', 'distmult',
           'distmultliteral', 'distmultliteralgated', 'ermlp', 'ermlpe', 'fixedmodel',
           'hole', 'inductivenodepiece', 'inductivenodepiecegnn', 'kg2e', 'mure',
           'nodepiece', 'ntn', 'pairre', 'proje', 'quate', 'rescal', 'rgcn',
           'rotate', 'se', 'simple', 'toruse', 'transd', 'transe', 'transf',
           'transh', 'transr', 'tucker', 'um']

class KnowledgeGraphEmbedding:
    def __init__(self, csvpath=None, split= None, model_name="TransE",
                 lr=0.001, embedding_dim=1024, n_epochs=5, batchsize=1024,
                 loss="bcewithlogits", negative_sampler='basic',
                 optimizer='SGD', training_loop='sLCWA', num_negs_per_pos=10):
        """
        Perform end-to-end knowledge graph embedding pipeline from triples factory.

        Parameters:
        - training (pykeen.triples.TriplesFactory): Triples factory for training.
        - testing (pykeen.triples.TriplesFactory): Triples factory for testing.
        - validation (pykeen.triples.TriplesFactory, optional): Triples factory for validation.
        - model_name (str, optional): Name of the knowledge graph embedding model to use.
                                       Default is "quate".
        - embedding_dim (int, optional): Dimensionality of the entity embeddings.
                                         Default is 1024.
        - n_epochs (int, optional): Number of epochs for training.
                                     Default is 10.
        - batchsize (int, optional): Batch size for training.
                                      Default is 1024.

        Returns:
        - pykeen.pipeline.PipelineResult: Result of the pipeline.
        """
        self.csvpath = csvpath
        self.split = split
        self.model_name = model_name
        self.lr = lr
        self.embedding_dim = embedding_dim
        self.n_epochs = n_epochs
        self.batchsize = batchsize
        self.loss = loss
        self.negative_sampler = negative_sampler
        self.optimizer = optimizer
        self.training_loop = training_loop
        self.num_negs_per_pos = num_negs_per_pos
        self.result = None

    def kge_end2end_pipeline(self):
        if self.csvpath is not None and self.split is not None:
           train, test, val = train_test_val_split_from_csv(self.csvpath, splits_ratio=self.split)
           torch.save(train, 'train')
           torch.save(test, 'test')
           torch.save(val, 'valid')
        elif self.csvpath is not None:
             # If split is None, use CSV directly as training data
           train = TriplesFactory.from_path(self.csvpath)
           test = None
           val = None
        else:
        # Load existing datasets if no CSV path is specified
           train = torch.load('train')
           test = torch.load('test')
           val = torch.load('valid')

        self.result = pipeline(
            model=self.model_name,
            random_seed=2000000,
            training=train,
            testing=test,
            validation=val,

            model_kwargs=dict(embedding_dim=self.embedding_dim, loss=self.loss),

            training_kwargs=dict(num_epochs=self.n_epochs, batch_size=self.batchsize),

            negative_sampler=self.negative_sampler,
            negative_sampler_kwargs={'num_negs_per_pos': self.num_negs_per_pos},
        )

    def save_results(self, directory_name='quate_gene', training_file='quate_training_gene'):
        if self.result is not None:
            self.result.save_to_directory(directory_name)
            torch.save(self.result.training, training_file)
        else:
            print("No result to save.")

    def display_metrics(self, metrics=['mean_rank', 'mean_reciprocal_rank'], hit_k=[1, 5, 10]):
        if self.result is not None:
            for m in metrics:
                print(f"{m}->{self.result.metric_results.get_metric(m)}")
            for k in hit_k:
                hits_at_k = self.result.metric_results.get_metric(f'hits_at_{k}')
                print(f"Hits@{k} -> ", hits_at_k)
        else:
            print("No result to display metrics.")
            """
            Display evaluation metrics.

            Parameters:
            - result (pykeen.pipeline.PipelineResult): Result of the pipeline.
            - metrics (list of str, optional): List of evaluation metrics to display.
                                               Default is ['mean_rank','mean_reciprocal_rank'].
            - hit_k (list of int, optional): List of values of k for hits@k metric.
                                             Default is [1,5,10].
            """

    def plot_training_error(self):
        if self.result is not None:
            plot(self.result)
        else:
            print("No result to plot training error.")
            """
            Plot the training error.

            Parameters:
            - result (pykeen.pipeline.PipelineResult): Result of the pipeline.
            """


def main():
    kg_embedding = KnowledgeGraphEmbedding(
        csvpath="R25KG-Rare2.tsv",
        model_name="quate",
        split=[0.8, 0.1, 0.1],
        lr=0.001,
        embedding_dim=1024,
        n_epochs=200,
        batchsize=1024,
        loss="bcewithlogits",
        negative_sampler='basic',
        training_loop='sLCWA',
        num_negs_per_pos=10
    )

    kg_embedding.kge_end2end_pipeline()
    kg_embedding.save_results()
    kg_embedding.display_metrics()
    kg_embedding.plot_training_error()


if __name__ == '__main__':
    main()

