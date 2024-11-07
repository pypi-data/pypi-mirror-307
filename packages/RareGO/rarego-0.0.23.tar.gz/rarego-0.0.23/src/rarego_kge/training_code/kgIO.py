import pykeen
from pykeen.triples import TriplesFactory
from pykeen.datasets import PathDataset
import pandas as pd

def process_input(input_data):
    """
    Process the input data to ensure it's a pandas DataFrame.

    Args:
        input_data: Either a file path (str) or a pandas DataFrame

    Returns:
        pandas.DataFrame: The processed data
    """
    if isinstance(input_data, pd.DataFrame):
        return input_data
    elif isinstance(input_data, str):
        return pd.read_csv(input_data)
    else:
        raise TypeError("Input must be a pandas DataFrame or a file path string")

def triple_factory_from_csv(input_data):
    """
    Create a TriplesFactory from either a CSV file path or a pandas DataFrame.

    Args:
        input_data: Either a file path (str) or a pandas DataFrame

    Returns:
        pykeen.triples.TriplesFactory: The created TriplesFactory
    """
    data = process_input(input_data)
    if isinstance(input_data, str):
        return TriplesFactory.from_path(input_data, create_inverse_triples=False)
    else:
        return TriplesFactory.from_labeled_triples(data.values, create_inverse_triples=False)

def pykeen_dataset_from_csv(input_data):
    """
    Create a PathDataset from either a CSV file path or a pandas DataFrame.

    Args:
        input_data: Either a file path (str) or a pandas DataFrame

    Returns:
        pykeen.datasets.PathDataset: The created PathDataset
    """
    if isinstance(input_data, str):
        return PathDataset.from_path(input_data)
    else:
        data = process_input(input_data)
        return PathDataset(triples=data.values)

def train_test_val_split_from_csv(input_data, splits_ratio=[0.8, 0.1, 0.1]):
    """
    Split the dataset into train, test, and validation sets.

    Args:
        input_data: Either a file path (str) or a pandas DataFrame
        splits_ratio (list): The splitting ratio for train, test, and validation sets

    Returns:
        tuple: (train, test, val) TriplesFactory objects
    """
    kg = triple_factory_from_csv(input_data)
    train, test, val = kg.split(splits_ratio)
    return train, test, val

def data_process(input_data, splits_ratio=[0.8, 0.1, 0.1]):
    """
    Process the input data and return various PyKEEN objects.

    Args:
        input_data: Either a file path (str) or a pandas DataFrame
        splits_ratio (list): The splitting ratio for train, test, and validation sets

    Returns:
        tuple: (triples_factory, dataset, train, test, val)
    """
    # Load the dataset as a TriplesFactory
    triples_factory = triple_factory_from_csv(input_data)
    
    # Load the dataset for grid search
    dataset = pykeen_dataset_from_csv(input_data)
    
    # Split the dataset
    train, test, val = train_test_val_split_from_csv(input_data, splits_ratio)
    
    return triples_factory, dataset, train, test, val

# Example usage:
#if __name__ == "__main__":
    # Using a CSV file path
    #csv_path = "path/to/your/csv_file.csv"
    #result_from_csv = data_process(csv_path)
    #print("Results from CSV:", result_from_csv)

    # Using a pandas DataFrame
    #df = pd.DataFrame
