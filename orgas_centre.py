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

            if len(list_query) == 3 : # Si query = cds
                list_subject = list[1].split("_")

                if len(list_subject) == 3 :#Si request = cds
                    liste_evalue.append(float(list[10]))
    return(liste_evalue)
    fichier.close()


path=os.listdir(dir)
liste_evalue = []

for file in path :
    #print(file)
    nom = file.split("_")[0]
    #transformer ca en switch case
    if file.startswith("SarbMEGA"):
        my_array0 = np.asarray(evalue_besthit(dir+"/"+file, liste_evalue)).astype(np.float)
    if file.startswith("SbayMEGA"):
        my_array1 = np.asarray(evalue_besthit(dir+"/"+file, liste_evalue)).astype(np.float)
    if file.startswith("ScerMEGA"):
        my_array2 = np.asarray(evalue_besthit(dir+"/"+file, liste_evalue)).astype(np.float)
    if file.startswith("SkudMEGA"):
        my_array3 = np.asarray(evalue_besthit(dir+"/"+file, liste_evalue)).astype(np.float)
    if file.startswith("SmikMEGA"):
        my_array4 = np.asarray(evalue_besthit(dir+"/"+file, liste_evalue)).astype(np.float)
    if file.startswith("SparMEGA"):
        my_array5 = np.asarray(evalue_besthit(dir+"/"+file, liste_evalue)).astype(np.float)
    #my_array = np.my_array(liste_evalue)
    #combien de besthit
print(len(my_array0))#206166
print(len(my_array1))#417473
print(len(my_array2))#655719
print(len(my_array3))#866444
print(len(my_array4))#1080582
print(len(my_array5))#1288200

data = [my_array0, my_array1, my_array2, my_array3, my_array4, my_array5]
#labels = ["SarbMEGA","SbayMEGA", "ScerMEGA", "SkudMEGA","SmikMEGA", "SparMEGA"]
for array in data:
    sns.distplot(array, hist = False, kde = True, kde_kws = {'linewidth':1} )

plt.legend(labels=["SarbMEGA","SbayMEGA","ScerMEGA""SkudMEGA", "SmikMEGA","SparMEGA"],prop={'size':10},title = "Organisme centré")
plt.title("Centered organisms")
plt.xlabel("evalue")
plt.ylabel("density")
plt.savefig("thelasttry2.png")

###############################################################################
############FINAL WORDS######################################################
