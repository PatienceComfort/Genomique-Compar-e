#!/usr/bin/python3

#L'objectif est de parser un fichier afin de recuperer uniquement les best hits (la première ligne suivant un #) dans un sens
import sys


file = sys.argv[1] #le 2eme argument correspond au fichier de blast output
nom_output = sys.argv[2] #le troisième argument correspond au nom du fichier où seront stockés nos résultats

fichier = open(file, "r") # Ouvrir le fichier de resultats blast
output = open(nom_output+".txt", "w") # Ouvrir le fichier resultat de notre parsing et le créer s'il n'existe pas
output.write("Voici le tableau récapitulant les données suivantes:\nquery_id\t subject_id\n" ) # Premiere ligne de notre resultat de parsing
i = iter(fichier)

ligne = fichier.readline() # Lire chaque ligne du fichier
for ligne in fichier: # Pour chaque ligne du fichier

    if ligne.startswith("#") :
        flag = False

    while (not ligne.startswith("#")) and (flag == False) :   
        list = ligne.split("\t") # L'inserer dans une liste ou chaque element est separe par un espace
        
        flag = True
        
        cons_query = list[0] # Prelever et conserver le query_id
        query_id = list[0]
        subject_id = list[1]

        # Prelever les données qui nous interessent sur la ligne suivante
        output.write(query_id+"\t"+subject_id +"\t\n") # L'inscrire dans notre output
        if list[0]==cons_query: # Comparer list[0] à notre valeur conservee de query_id
            next(i) # Si ca correspond, passer a la ligne suivante
        else:
            cons_query = list[0]#sinon list[0] remplace la valeur conservee de query_id

# Fermer les fichiers blast et output
fichier.close()
output.close()

#Dans cette version, on ontient les best hits MAIS, parfois (souvent), le best hit est un blast de la séquence contre elle meme (donc eco_1 vs eco_1) ce qui a peu d'intéret pour nous à mon avis
#Dans la prochaine version, nous voulons un script qui permetterai de s'affanchir de la première ligne si elle s'avère etre une autoblast
