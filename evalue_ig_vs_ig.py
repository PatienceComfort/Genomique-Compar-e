#!/usr/bin/python3


import sys, os, matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

dir = sys.argv[1]

def evalue_besthit(file, liste_evalue) :
    fichier = open(file, "r") # Ouvrir le fichier de resultats blast

    for ligne in fichier : # Pour chaque ligne du fichier
        if ligne.startswith("#") :
            flag = False # Pas de besthit catch

        elif (flag==False) :
            list = ligne.split("\t")
            list_query = list[0].split("_")

            if len(list_query) == 4 : # Si query = igorf
                list_subject = list[1].split("_")

                if len(list_subject) == 4 :#Si request = igorf
                    liste_evalue.append(float(list[10]))
    return(liste_evalue)
    fichier.close()


path=os.listdir(dir)
liste_evalue = []

for file in path :
    #print(file)
    my_array = np.asarray(evalue_besthit(dir+"/"+file, liste_evalue)).astype(np.float)
    #my_array = np.my_array(liste_evalue)
print(len(my_array))

#plt.xlim([min(liste_evalue), max(liste_evalue)])
#plt.plot(my_array, bin = 10,range = (my_array.min(), my_array.max()) )#range = (my_array.min(), my_array.max())
#plt.ylabel('Fréquence')
#plt.xlabel('evalue')
#plt.savefig('ig_vs_ig_final.pdf')
#plt.show()

#seaborn density
sns.displot(my_array,  kind="kde")#fig =
plt.xlabel("evalue")#fig.set
plt.title("IGORF VS IGORF")
plt.savefig("thelastfuckingtimeisg.pdf")#fig.savefig
