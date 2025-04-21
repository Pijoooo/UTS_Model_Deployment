import zipfile
import os
import pickle

def load_pickle(zip_path):
    # Make sure we're in the right base directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    zip_path = os.path.join(base_dir, zip_path)

    # Check if file exists
    if not os.path.exists(zip_path):
        raise FileNotFoundError(f"File not found: {zip_path}")

    if zip_path.endswith(".zip"):
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(base_dir)  # Extract to the script's directory
            for name in zip_ref.namelist():
                if name.endswith(".pkl"):
                    pkl_path = os.path.join(base_dir, name)
                    with open(pkl_path, "rb") as f:
                        obj = pickle.load(f)
                    # Optionally remove the extracted .pkl to keep things clean
                    os.remove(pkl_path)
                    return obj
        raise ValueError("No .pkl file found in the zip archive.")
    else:
        with open(zip_path, "rb") as f:
            return pickle.load(f)
