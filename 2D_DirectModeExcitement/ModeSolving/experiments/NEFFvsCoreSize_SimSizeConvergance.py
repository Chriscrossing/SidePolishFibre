import meep as mp
import numpy as np
import matplotlib.pyplot as plt
import csv

"""
todo:- 

each device has to have: 

- quick plot of structure and field with 1d cross section. x
        - raw data in .h5 x
        - raw image of structure and field in png. x

- neff vs temp, in quick plot and csv. x


"""

class experiment:

    def __init__(self,Model):
        
        self.Model = Model
        self.Variables = Model.structure.Variables
        fig,ax = plt.subplots(dpi=200)


        self.WL = np.array([1.55499,1.555,1.55501])
        self.Variables['R1'] = 0.5

        self.Simsize = [50,100,125,150]
        

        self.MDNI_D = np.array([])

        for Size in self.Simsize:
            self.Variables['SimSize'] = Size
            self.runMDNI()
            self.MDNI_D = np.append(self.MDNI_D,self.d)

        ax.plot(self.Simsize,self.MDNI_D)

        #self.myCSVwriter()

        #ax.legend()
        ax.set_xlabel("Simsize / um")
        ax.set_ylabel("Dispersion  ps / (nm)(km)")

        #plt.savefig(self.Variables['workingDir']+"NeffvsWL.pdf")
        plt.show()
        #self.myCSVwriter()



    def runSMF28(self):
        self.Variables['Datafile']  = "SMF28"
        neff  = []
    
        self.Variables['nCore'] = 1.45077  # 1.445
        self.Variables['R2'] = 62.5

        #self.Model.SolveModeProfile()


        for wl in self.WL:
            print("==============================")
            print("==============================")
            print("==============================")
            print("Set WL:", wl)
            print("==============================")
            print("==============================")
            print("==============================")
            self.Variables['wl'] = wl
            self.Model.SolveEffectiveIndex()
            neff.append(self.Model.structure.neff)

        self.d = self.Centraldispersion(self.WL,neff)
        
        

    def runMDNI(self):
        self.Variables['Datafile']  = "MDNI"
        neff  = np.array([])

        self.Variables['nCore'] = 1.62  # 1.445

        #self.Model.SolveModeProfile()


        for wl in self.WL:
            print("==============================")
            print("==============================")
            print("==============================")
            print("Set WL:", wl)
            print("==============================")
            print("==============================")
            print("==============================")
            self.Variables['wl'] = wl
            self.Model.SolveEffectiveIndex()
            neff = np.append(neff,self.Model.structure.neff)

        self.d = self.Centraldispersion(self.WL,neff)
        

    def runMAPbBr3(self):
        self.Variables['Datafile']  = "MAPbBr3"
        self.MAPbBr3neff  = []

        self.Variables['nCore'] = 2.24
        #self.Model.SolveModeProfile()


        for wl in self.WL:
            print("==============================")
            print("==============================")
            print("==============================")
            print("Set WL:", wl)
            print("==============================")
            print("==============================")
            print("==============================")
            self.Variables['wl'] = wl
            self.Model.SolveEffectiveIndex()
            self.MAPbBr3neff.append(self.Model.structure.neff)


        
        self.ax.plot(self.WL,self.MAPbBr3neff,label="MAPbBr3")



    def wlFunc(self,wl):
        items = len(wl)-1 
        new = np.zeros(items)
        for i in range(0,items):
            new[i] = (wl[i+1] + wl[i])/2        
        return new



    def Centraldispersion(self,wl,neff):
        #wl needs to be in microns
        
        wl = 1000*np.array(wl) # convert to nm
        neff = np.array(neff)


        
        
        dydx = np.diff(neff)/np.diff(wl)
        newWl = self.wlFunc(wl)
        #plt.plot(newWl,dydx)

        
        d2ydx2 = np.diff(dydx)/np.diff(newWl)
        finalWL = self.wlFunc(newWl)

        return (-finalWL/299792458.0) * d2ydx2 * 1e15
        



    def myCSVwriter(self):
        with open(self.Variables['workingDir'] + 'neff.csv', 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            
            
            spamwriter.writerow(["Resolution","MDNI D"])
            
            for i in range(len(self.coreRadius)):
                spamwriter.writerow([self.resolution[i],self.MDNI_D[i]])