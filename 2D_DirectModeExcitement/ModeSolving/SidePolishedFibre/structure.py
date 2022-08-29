import meep as mp
import numpy as np
from datetime import date
import matplotlib.pyplot as plt

class structure:


    '''
    initialise structure class with a variable dictionary:
    '''

    def __init__(self):
        self.Variables = {
			#programming vars 
			"debug":False,
			"prevRun":False,
            "SimTime":0.0,
			#refractive indexes
            "Tdependance":False,
            "T":20,
			"nAir": 1.000,
			"nCore":1.445,
			"nClad":1.440,
			"nCoating":1.410,
            "setCoating":"Air",
			#Device Dimentions
			"R1":4.1,
            "R2":62.5,
            "CladLeft":1.0,
            "Polished":True,
			##Resonator Dimentions
            'FibreType':"Polished",
            'angle':121.4,
            'CladLeft':0 ,
            'Depth':40,
            'Width':30,#:322,
            'GAP':60,#:500,
            
            'BubblesNum':2 ,
            'BubblesType':'sqr',
            'FibreType':'Polished',
			#Simulation area Properties
            "sy":20,
			'PAD':15,
			"res":10,    # would usually be 10px per wl but our smallest waveguide is 1um thick
			"dpml":1.55,
			#Simulation source Properties
			"wl":1.55,
			"WLres":0.1/1000, #res in um so 100pm
			"Courant":1.000/np.sqrt(2.000),
			#Simulation Properties
			"today":str(date.today()),
			"WallT":0,
			"workingDir":'../data/',
            'Datafile':"",
			"roundTrips":1.00,    #relates to how long the sim will run relative to orbits of the WGM
			"SaveFieldsatEnd":True,
            #Flags
			"normal":True,
			"savefields":False
		}

        #self.PDMSindex()
        #self.Silicaindex()
        

        #make objects


    def buildStructure(self):

        print("in SidePolishedFibre/structure.py")
        
        self.Objlist = []

        if self.Variables['setCoating'] == "PDMS":
            self.Variables['nCoating'] = self.PDMSindex(self.Variables['T'])
        elif self.Variables['setCoating'] == "Air":
            self.Variables['nCoating'] = self.Variables['nAir']

        if self.Variables['FibreType']   == "Polished":
            if self.Variables['Tdependance'] == True:
                self.Variables['nCore']    = self.Silicaindex(self.Variables['T'],n0 = 1.45077)
                self.Variables['nClad']    = self.Silicaindex(self.Variables['T'],n0 = 1.4440)
                
                
            self.buildPolishedFibre()
            

        elif self.Variables['FibreType'] == "unpolished":
            if self.Variables['Tdependance'] == True:
                
                self.Variables['nCore'] = self.Silicaindex(self.Variables['T'],n0 = 1.45077)
                self.Variables['nClad'] = self.Silicaindex(self.Variables['T'],n0 = 1.4440)
            self.buildUnpolishedFibre()
        
        else:
            print("Fibre Type not selected")


    """
    Build a side polished fibre with two dips, with set angles and set GAP.
    """


    def buildPolishedFibre(self):
        #Build a structure that represents a system without the device, i.e here i've just built a waveguide 
        #without a WGM.
        self.Objlist = []
        
        self.Variables["sx"] = self.Variables['GAP'] - self.Variables['Width'] +   self.Variables['PAD']   +   2*self.Variables['dpml']

        #self.Variables["sx"] = self.Variables['GAP']    +   2*self.Variables['Width']   +   self.Variables['PAD']   +   2*self.Variables['dpml'] + 100
        #self.Variables["sy"] = 2.3*self.Variables['R2'] + 2*self.Variables['dpml'] #20 + 2*self.Variables['dpml'] #
		
        self.cell_size = mp.Vector3(self.Variables["sx"],self.Variables["sy"],0)

        self.pml_layers = [mp.PML(thickness=self.Variables["dpml"])]

        self.Coating = mp.Block(
            center=mp.Vector3(0,0,0),
            size=mp.Vector3(mp.inf,mp.inf,mp.inf),
            material=mp.Medium(index=self.Variables['nCoating'])
            )


        self.Clad = mp.Block(
            center=mp.Vector3(x=0,y=(-self.Variables['R2']/2 + self.Variables['CladLeft']/2 + self.Variables['R1']/2)),
            size=mp.Vector3(x=mp.inf,y= self.Variables['R2'] + self.Variables['R1'] + self.Variables['CladLeft']   ,z=mp.inf),
            material=mp.Medium(index=self.Variables['nClad'])
            )

        self.Core = mp.Block(
            center=mp.Vector3(0,0,0),
            size=mp.Vector3(mp.inf,2*self.Variables['R1'],mp.inf),
            material=mp.Medium(index=self.Variables['nCore'])
            )


        TL    = self.Variables['Width']
        D     = self.Variables['Depth']
        angle = self.Variables['angle']

        BL    = TL - 2*(D/np.tan((180-angle)*(np.pi/180)))
                
        verts = [
                
                mp.Vector3(x=-TL/2,		y=D 	,z=0),
                mp.Vector3(x=TL/2 ,		y=D 	,z=0),
                mp.Vector3(x=BL/2 ,		y=0 	,z=0),
                mp.Vector3(x=-BL/2,		y=0 	,z=0)
            
                ]


        self.LH = mp.Prism(center=mp.Vector3(       x=-self.Variables['GAP']/2     ,y=-D/2+self.Variables['R1']+self.Variables['CladLeft'],z=0),
                            vertices = verts,
                            material=mp.Medium(index=self.Variables['nCoating']),
                            height=1
                            )

        self.RH = mp.Prism(center=mp.Vector3(       x=self.Variables['GAP']/2       ,y=-D/2+self.Variables['R1']+self.Variables['CladLeft'],z=0),
                            vertices = verts,
                            material=mp.Medium(index=self.Variables['nCoating']),
                            height=1
                            )

        self.Objlist.extend([self.Coating,self.Clad,self.Core,self.LH,self.RH])
    
    '''
    BuildModel_CW is used to build the MEEP simulation object with a source.
    '''

    def BuildModel(self):   # builds sim and plots structure to file

        self.fcen = 1/self.Variables['wl']
        self.df = 0.1*self.fcen
        self.kpoint = mp.Vector3(x=0, y=0, z=self.fcen*self.Variables['nCore'])


        self.src = [
            mp.Source(mp.GaussianSource(self.fcen, 
                fwidth=self.df), 
                mp.Ez, 
                mp.Vector3(0),
                size=mp.Vector3(y=8.2)
                )
            ]

        self.sim = mp.Simulation(
                cell_size=self.cell_size,
                geometry=self.Objlist,
                sources=self.src,
                resolution=self.Variables['res'],
                symmetries=[mp.Mirror(mp.X)],
                force_complex_fields=True,
                eps_averaging=True,
                boundary_layers=self.pml_layers,
                k_point=self.kpoint,
                ensure_periodicity=False
            )


        subdir = ""
        if self.Variables['Datafile'] != "":
            subdir = "/" + self.Variables['Datafile'] 
        
        self.sim.use_output_directory(self.Variables['workingDir'] + subdir)


        self.Variables['MPsimname'] = self.sim.get_filename_prefix()

        
        fig,ax = plt.subplots()
        
        self.sim.plot2D(
            ax=ax,
            #output_plane=mp.Volume(center=mp.Vector3(),size=mp.Vector3(self.SimSize,self.SimSize)),
            #fields=mp.Ez,
            plot_sources_flag=True,
            plot_monitors_flag=False,
            plot_eps_flag=True,
            eps_parameters={'alpha': 0.8, 'interpolation': 'none'}
        )
        plt.savefig(self.Variables['workingDir']+"Structure" + str(self.Variables['Datafile']) + ".pdf")
        print("here!")
        plt.show()
        #plt.close()


    """
    RunMPB solves for k, group velocity and neff. 
    """

    def RunMPB(self):

        self.sim.init_sim()

        self.EigenmodeData = self.sim.get_eigenmode(
                self.fcen,
                mp.Z,
                        mp.Volume(center=mp.Vector3(), size=mp.Vector3(
                            self.SrcSize, self.SrcSize, 0)),
                band_num=self.Variables['band_num'],
                kpoint=self.kpoint,
                match_frequency=True,
                resolution=self.Variables['res']
            )

        self.k = self.EigenmodeData.k
        self.vg = self.EigenmodeData.group_velocity
        self.neff = self.k.norm() * 1/self.fcen
        

            
    def PDMSindex(self,temp):

        PDMStemp = np.array([27.04200613, 30.04708872, 40.09978324, 50.0485836, 60.10202556, 70.05194708, 80.00074744])
        nPDMS    = np.array([1.410413147,1.409271947,1.405629718,1.4019877,1.398453453,1.394973372,1.391331424])
        PDMSfit = np.polyfit(PDMStemp,nPDMS,deg=1)
        return np.polyval(PDMSfit,temp)




    def Silicaindex(self,T,n0):
        T0 = 20 
        dndT = 12.0791e-6 # T Toyoda and M Yabe 1983 J. Phys. D: Appl. Phys. 16 L97
        return dndT*(T-T0) + n0
            
        
