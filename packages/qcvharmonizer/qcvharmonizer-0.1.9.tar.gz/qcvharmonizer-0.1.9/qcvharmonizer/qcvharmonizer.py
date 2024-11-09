import os
from typing import Union
from glob import glob 
from datetime import date
from time import time 
import cerbere
import xarray as xr

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)




def harmonize(ds: Union[xr.Dataset, str], **kwargs):
    """
    Harmonize the incoming dataset according to FAIR EASE QCV specifications.

    This function processes and harmonizes a dataset (`ds`) based on the input 
    specifications, following the FAIR (Findable, Accessible, Interoperable, 
    and Reusable) and EASE (Environmental, Agricultural, and Societal Ecosystems) 
    QCV (Quality Control and Validation) standards. It utilizes the `cerbere` 
    library's `open_dataset` function to load and harmonize the dataset, adjusting 
    it for compliance with these standards.

    Args:
        ds (str, xr.Dataset): The input dataset. It can either be a file path 
            (string) or an already opened `xarray.Dataset`.
        **kwargs (dict): Additional keyword arguments passed to the `open_dataset`
            function. This can include:
                - 'reader' (optional): Specifies a custom reader function or 
                    strategy for opening the dataset.
                - Other keyword arguments will be forwarded to `open_dataset`.

    Returns:
        xr.Dataset: The harmonized dataset as an `xarray.Dataset` object, 
        adjusted according to the FAIR and EASE QCV specifications.

    Example:
        harmonized_ds = harmonize("data.nc", reader="custom_reader", param1=value)
        
    Notes:
        - The function relies on the `cerbere.open_dataset()` function for the actual
            opening and harmonization of the dataset.
        - If no custom reader is provided, the default reader will be used.
    """    
    reader = kwargs.pop('reader', None)
    harmonized_dataset = cerbere.open_dataset(ds, reader=reader, **kwargs)
    
    return harmonized_dataset


# - - - - main.py - - - -
if __name__ == "__main__":
    # version manuelle : 
    files = glob('/runtime/data/EXT/ARGO/content/202212-ArgoData/dac/coriolis/6901580/profiles/B*.nc')
    [files.append(elem) for elem in glob('/runtime/data-in/profiles/D*.nc')]
    [files.append(elem) for elem in glob('/runtime/data-in/profiles/R*.nc')]

    files = files[0:10]

    meta_file = glob('/runtime/data/EXT/ARGO/content/202212-ArgoData/dac/coriolis/6901580/*6901580*meta*.nc')[0]
    c = 0
    for f in files :    
        
        start = time()
        ds = harmonize(f, meta_file=None, reader="POKARGO")
        end = time()
        print(f"        {c}/{len(files)}  - time for loop : ", round(end-start, 2), " seconds - " , os.path.basename(f).replace('.nc', ''))
        c+=1