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

        self.WL= np.arange(1.5,1.6,0.01)

        fig,self.ax = plt.subplots(dpi=200)

        self.runSMF28()
        self.runMDNI()
        self.runMAPbBr3()

        self.myCSVwriter()

        self.ax.legend()
        self.ax.set_xlabel("WL / um")
        self.ax.set_ylabel("Neff")

        plt.savefig(self.Variables['workingDir']+"NeffvsWL.pdf")



    def runSMF28(self):
        self.Variables['Datafile']  = "SMF28"
        self.SMF28neff  = []

        self.Variables['nCore'] = 1.45077  # 1.445
        self.Variables['R1'] = 4.1
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
            self.SMF28neff.append(self.Model.structure.neff)


        
        self.ax.plot(self.WL,self.SMF28neff,label="SMF28")


    def runMDNI(self):
        self.Variables['Datafile']  = "MDNI"
        self.MDNIneff  = []

        self.Variables['R1'] = 2.5
        self.Variables['nCore'] = 1.62

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
            self.MDNIneff.append(self.Model.structure.neff)


        
        self.ax.plot(self.WL,self.MDNIneff,label="MDNI")
        

    def runMAPbBr3(self):
        self.Variables['Datafile']  = "MAPbBr3"
        self.MAPbBr3neff  = []
        
        self.Variables['R1'] = 2.5
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

        

    def myCSVwriter(self):
        with open(self.Variables['workingDir'] + 'neff.csv', 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            
            
            spamwriter.writerow(["WL / um","SMF-28 Ultra NEFF","MDNI NEFF","MAPbBr3 NEFF"])
            
            for i in range(len(self.WL)):
                spamwriter.writerow([self.WL[i],self.SMF28neff[i],self.MDNIneff[i],self.MAPbBr3neff[i]])