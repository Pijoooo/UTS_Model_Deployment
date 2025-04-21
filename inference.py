import zipfile
import os
import pickle

def load_pickle(file):
    base_dir = os.path.dirname(__file__)  # same directory as script
    file_path = os.path.join(base_dir, file)

    if file.endswith(".zip"):
        with zipfile.ZipFile(file_path, "r") as zip_ref:
            zip_ref.extractall(base_dir)
            for name in zip_ref.namelist():
                if name.endswith(".pkl"):
                    pkl_path = os.path.join(base_dir, name)
                    with open(pkl_path, "rb") as f:
                        obj = pickle.load(f)
                    os.remove(pkl_path)
                    return obj
    else:
        with open(file_path, "rb") as f:
            return pickle.load(f)
