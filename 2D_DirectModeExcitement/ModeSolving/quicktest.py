import meep as mp
import numpy as np
from matplotlib import pyplot as plt
from IPython.display import Video

import SidePolishedFibre.structure as structure

fcen=1/1.55

df=0.06

device = structure.structure()
device.Variables['GAP'] = 500
device.Variables['Width'] = 322
device.Variables['PAD'] = 1000
device.Variables['sy'] = 30
device.Variables['setCoating'] = "PDMS"
device.Variables['angle'] =90   
device.buildStructure()




src = [mp.Source(mp.GaussianSource(fcen, fwidth=df), mp.Ey, mp.Vector3(0),size=mp.Vector3(y=0))]

sym = [mp.Mirror(mp.X, phase=1)]

sim = mp.Simulation(
    cell_size=device.cell_size,
    geometry=device.Objlist,
    boundary_layers=device.pml_layers,
    eps_averaging=True,
    sources=src,
    symmetries=sym,
    resolution=10,
    )



h = mp.Harminv(mp.Ey, mp.Vector3(), fcen, df)



sim.run(mp.after_sources(h), until_after_sources=2*device.Variables['sx'])


f = [m.freq for m in h.modes]
Q = [m.Q for m in h.modes]

for fiter, qiter in zip(f, Q):
    print(f"Resonant Wavelentgh (um): {1/fiter}, Q: {qiter}")