import pandas as pd
import glob
from tqdm import tqdm
import pickle
from pathlib import Path
import timeit

def make_unsplash(new=False):
    pth = Path("./data/unsplash.pickle")
    if Path.exists(pth) and not new:
        fin = open(pth,'rb')
        unsp = pickle.load(fin)
        return unsp
    unsp = Unsplash()
    unsp.get_data()
    pickle.dump(unsp, open(pth, 'wb'))
    return unsp

class Unsplash:
    def __init__(self):
        self.path = './data/'
        self.documents = ['photos', 'keywords', 'colors']
        self.datasets = {}

    def get_data(self):
        for doc in tqdm(self.documents):
            files = glob.glob(self.path + doc + ".tsv*")
            subsets = []
            for filename in files:
                df = pd.read_csv(filename, sep='\t', header=0)
                subsets.append(df)
            self.datasets[doc] = pd.concat(subsets, axis=0, ignore_index=True)

    def get_random_img(self):
        samp_data = self.datasets["photos"].sample()
        return samp_data.iloc[0]["photo_id"]

    def to_sql(self, engine):
        for fn in self.documents:
            self.datasets[fn].reset_index(drop=True,inplace=True)
            self.datasets[fn].to_sql(f"unsplash_{fn}", con=engine, if_exists='append')