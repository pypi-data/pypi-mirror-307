import pandas as pd
from importlib import resources

def list_csv_files():
    data_files = []
    package_dir = resources.files('rarego_kge.data')
    for file in package_dir.iterdir():
        if file.suffix in ['.csv', '.tsv']:
            data_files.append(file.name)
    return data_files

def read_csv_file(filename):
    if not (filename.endswith('.csv') or filename.endswith('.tsv')):
        raise ValueError("File must be a CSV or TSV")
    
    package_dir = resources.files('rarego_kge.data')
    file_path = package_dir / filename
    
    # Determine the separator based on file extension
    separator = '\t' if filename.endswith('.tsv') else ','
    
    with file_path.open('r') as file:
        df = pd.read_csv(file,names=['H','R','T'], sep=separator)
    return df