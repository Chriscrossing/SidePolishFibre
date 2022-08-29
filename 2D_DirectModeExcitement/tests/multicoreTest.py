import meep as mp
import numpy as np
from matplotlib import pyplot as plt
from IPython.display import Video


def simulation():

    fcen=1/1.55

    df=0.06
    resolution = 10  # pixels/um

    core = 1.444*2  # dielectric constant of waveguide

    w = 8.2 # width of waveguide


    dpml = 1  # PML thickness

    L = 1000

    dwL = 5

    pad = 2

    sx = 2 * (pad + dpml + dwL) + L  # size of cell in x direction

    sy = 2 * (pad + dpml) + w 

    cell = mp.Vector3(sx, sy, 0)


    cavity = mp.Block(
        size=mp.Vector3(L, w, mp.inf), 
        material=mp.Medium(epsilon=core)
        )

    geometry = [cavity]
    pml_layers = [mp.PML(1.0)]

    src = [mp.Source(mp.GaussianSource(fcen, fwidth=df), mp.Ez, mp.Vector3(0),size=mp.Vector3(y=8.2))]

    sym = [mp.Mirror(mp.Y, phase=1), mp.Mirror(mp.X, phase=1)]

    sim = mp.Simulation(
        cell_size=cell,
        geometry=geometry,
        boundary_layers=pml_layers,
        eps_averaging=False,
        sources=src,
        symmetries=sym,
        resolution=resolution,
        )
    
    h = mp.Harminv(mp.Ez, mp.Vector3(), fcen, df)
    sim.run(mp.after_sources(h), until_after_sources=5000)

    f = [m.freq for m in h.modes]
    Q = [m.Q for m in h.modes]

    for fiter, qiter in zip(f, Q):
        print(f"Resonant Wavelentgh (um): {1/fiter}, Q: {qiter}")


simulation()


