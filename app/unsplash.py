import pandas as pd
import glob
from tqdm import tqdm
from pathlib import Path

class Unsplash:
    def __init__(self):
        path = './data/'
        self.documents = ['photos', 'keywords', 'colors']
        self.datasets = {}

        for doc in tqdm(self.documents):
            files = glob.glob(path + doc + ".tsv*")
            subsets = []
            for filename in files:
                df = pd.read_csv(filename, sep='\t', header=0)
                subsets.append(df)
            self.datasets[doc] = pd.concat(subsets, axis=0, ignore_index=True)

    def get_random_img(self):
        samp_data = self.datasets["photos"].sample()
        return samp_data.iloc[0]["photo_id"]
