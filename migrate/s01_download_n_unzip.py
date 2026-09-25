#imports
import requests, zipfile, io, os, psycopg2
from pathlib import Path
import pandas as pd
import numpy as np
from psycopg2.extras import execute_values
from psycopg2 import sql
from s02_init_db import connect_with_retry 
from dotenv import load_dotenv


#methods
def get_base_fn(file_path):
    base_name, _ = os.path.splitext(file_path)
    return base_name

def change_extension(file_path, new_extension):
    # base_name, _ = os.path.splitext(file_path)
    base_name = get_base_fn(file_path)
    new_file_path = base_name + "." + new_extension
    os.rename(file_path, new_file_path)
    print(f"{file_path} is now {new_file_path}" )
    
# variables
root = Path()

# create folder inside root, called data
# create folder inside root/data called static
#creating data storage folders in root
data_folder = 'data'
data_pth = root / data_folder
data_pth.mkdir(parents=True, exist_ok=True)
static_folder = 'static'
static_pth = data_pth / static_folder
static_pth.mkdir(parents=True, exist_ok=True)

# download gtfs.zip from https://data.foli.fi/gtfs/gtfs.zip and place inside data.
# unzip data/gtfs.zip into static.
zip_url =  r'https://data.foli.fi/gtfs/gtfs.zip'
r = requests.get(zip_url, stream=True)
z = zipfile.ZipFile(io.BytesIO(r.content))
z.extractall(static_pth)

# rename all files to suffix .csv
for f in static_pth.iterdir():
    if f.name.endswith('.txt'):
        change_extension(f, 'csv')



