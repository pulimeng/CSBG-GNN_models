import os.path as osp
import h5py

import torch
from torch_geometric.data import Data, Dataset

def LoadData(path):
    with h5py.File(path, 'r') as f:
        X = f['X'][()]
        eI = f['eI'][()]
        eAttr = f['eAttr'][()]
        y = f['y'][()]
    X = torch.tensor(X, dtype=torch.float32)
    eI = torch.tensor(eI, dtype=torch.long)
    eAttr = torch.tensor(eAttr, dtype=torch.float32)
    y = torch.tensor(y, dtype=torch.long)
    data = Data(x=X, edge_index=eI, edge_attr=eAttr, y=y)
    return data

class MyGraphDataset(Dataset):
    def __init__(self, root, df, device):
        super(MyGraphDataset, self).__init__(root, df)
        self.root = root
        self.df = df
        self.device = device
        
    def __len__(self):
        return len(self.df)
    
    def __getitem__(self, idx):
        filename = self.df.loc[idx, 'filename'] # TODO: change this line accordingly
        data = torch.load(osp.join(self.root, filename))
        return data