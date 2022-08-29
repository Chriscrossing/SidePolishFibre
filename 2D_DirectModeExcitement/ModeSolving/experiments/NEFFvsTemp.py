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


        self.Variables['Tdependance'] = True
        self.temps= [20,30,40,50,60,70,80,90,100]

        fig,self.ax = plt.subplots(dpi=200)

        self.runSMF28()
        self.runPolishedAir()
        self.runPolishedPDMS()
        self.myCSVwriter()

        self.ax.legend()
        self.ax.set_xlabel("Temp / C")
        self.ax.set_ylabel("Neff")

        plt.savefig(self.Variables['workingDir']+"NeffvsTemp.pdf")

        fig,self.ax = plt.subplots(dpi=200)

        self.ax.plot(self.temps,np.array(self.PolishedAirneff)-np.array(self.SMF28neff),label="Polished SMF-28 Air Coated")
        self.ax.plot(self.temps,np.array(self.PolishedPDMSneff)-np.array(self.SMF28neff),label="Polished SMF-28 PDMS Coated")

        self.ax.legend()
        self.ax.set_xlabel("Temp / C")
        self.ax.set_ylabel("\Delta Neff Compared to smf-28")

        plt.savefig(self.Variables['workingDir']+"deltaNeff.pdf")






    def runSMF28(self):
        self.Variables['FibreType'] = "unpolished"
        self.Variables['Datafile']  = "smf28"
        self.SMF28neff  = []

        self.Variables['T'] = 20

        #self.Model.SolveModeProfile()


        for T in self.temps:
            print("Set Temp:", T)
            self.Variables['T'] = T
            self.Model.SolveEffectiveIndex()
            self.SMF28neff.append(self.Model.structure.neff)


        
        self.ax.plot(self.temps,self.SMF28neff,label="SMF-28")
        

    def runPolishedAir(self):
        self.Variables['FibreType'] = "Polished"
        self.Variables['Datafile']  = "PolishedAir"
        self.Variables['setCoating'] = "Air" 
        self.PolishedAirneff  = []

        self.Variables['T'] = 20

        #self.Model.SolveModeProfile()

        for T in self.temps:
            print("Set Temp:", T)
            self.Variables['T'] = T
            self.Model.SolveEffectiveIndex()
            self.PolishedAirneff.append(self.Model.structure.neff)

        


        self.ax.plot(self.temps,self.PolishedAirneff,label="Polished SMF-28 Air Coated")

    def runPolishedPDMS(self):
        self.Variables['FibreType'] = "Polished"
        self.Variables['Datafile']  = "PolishedPDMS"
        self.Variables['setCoating']= "PDMS" 
        self.PolishedPDMSneff  = []

        self.Variables['T'] = 20

        #self.Model.SolveModeProfile()

        for T in self.temps:
            print("Set Temp:", T)
            self.Variables['T'] = T
            self.Model.SolveEffectiveIndex()
            self.PolishedPDMSneff.append(self.Model.structure.neff)

        
        
        self.ax.plot(self.temps,self.PolishedPDMSneff,label="Polished SMF-28 PDMS Coated")
        

    def myCSVwriter(self):
        with open(self.Variables['workingDir'] + 'neff.csv', 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            
            
            spamwriter.writerow(["Temp / C","SMF-28 NEFF","Polished SMF-28 Air Coated NEFF", "Polished PDMS Coated NEFF"])
            
            for i in range(len(self.temps)):
                spamwriter.writerow([self.temps[i],self.SMF28neff[i],self.PolishedAirneff[i],self.PolishedPDMSneff[i]])