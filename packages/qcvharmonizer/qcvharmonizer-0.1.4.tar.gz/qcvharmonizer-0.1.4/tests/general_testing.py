import qcvharmonizer 
from glob import glob 

# version manuelle : 
files = glob('/runtime/data/EXT/ARGO/content/202212-ArgoData/dac/coriolis/6901580/profiles/B*.nc')
[files.append(elem) for elem in glob('/runtime/data-in/profiles/D*.nc')]
[files.append(elem) for elem in glob('/runtime/data-in/profiles/R*.nc')]

file = files[7]
ds = qcvharmonizer.harmonize(file, meta_file=None, reader="POKARGO")