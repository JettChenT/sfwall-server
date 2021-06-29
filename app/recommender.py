def make_recommender(fname):
    f = h5py.File(fname,"r")
    cosine_sim = f["cosine_sim"]
    id_data = pd.read_hdf(fname,"/data/id")
    return Recommender(cosine_sim,id_data)
