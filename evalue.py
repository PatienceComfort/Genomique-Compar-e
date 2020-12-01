import sys, os, matplotlib.pyplot as plt

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

                if len(list_subject) == 4 :
                    liste_evalue.append(list[10])
    fichier.close()


path=os.listdir(dir)
liste_evalue = []

for file in path :
    print(file)
    evalue_besthit(dir+"/"+file, liste_evalue)



plt.xlim([min(liste_evalue)-5, max(liste_evalue)+5])
plt.hist(liste_evalue)

plt.show()


