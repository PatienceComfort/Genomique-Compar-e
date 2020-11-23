#!/usr/bin/python3
"""
Author : Hugues Herrmann
Purpose : 
Date : 21/11/20
"""

import sys, os


directory = sys.argv[sys.argv.index("-file")+1]


def besthit(directory, blast_output) :
# Parcourt un output de blast et ecrie le besthit dans un nouveau fichier output
# Un fichier output_blast + le repertoire dans lequel se trouve le fichier
# Un fichier .txt contenant les besthits 

    input = open(directory + "/" + blast_output, "r") # Ouvrir le fichier de resultats blast
    output = open(blast_output.split(".")[0] + ".txt", "w") # Ouvrir le fichier output portant le meme nom que le fichier input

    for ligne in input : # Pour chaque ligne du fichier

        if ligne.startswith("#") :
            flag = False # False = le best hit n'a pas encore ete trouve

        while (not ligne.startswith("#")) and (flag == False) : # Tant qu'on a pas de best hit  
            list = ligne.split("\t") # Liste des resultats du best hit
            
            flag = True # Best hit trouve
            
            query_id = list[0]
            subject_id = list[1]
            identity = list[2]
            e_value = list[11]
            
            output.write(query_id+"\t"+subject_id +"\t"+identity+"\t"+e_value+"\t\n") # Ecrire les stats du best hit
            
    input.close()
    output.close()



def parse_blast(directory, fichier_blast, dGen, eval, id) :
    file = open(directory + "/" + fichier_blast, "r")
    lignes = file.readlines()
    file.close()

    name = fichier_blast.split("-")[0] # Le nom de l'espece blastee

    if not name in dGen["name"] : # Liste des noms des especes
        dGen["name"].append(name)
        dGen[name] = {}
        dGen[name]["query"] = []

    for ligne in lignes :
        ligne = ligne.split()

        if float(ligne[2])>=id and float(ligne[3])<eval :
            if not ligne[0] in dGen[name]["query"] :
                dGen[name]["query"].append(ligne[0])
                dGen[name][ligne[0]] = {}
                dGen[name][ligne[0]]["subject"] = []
                dGen[name][ligne[0]]["subject"].append(ligne[1])
            elif not ligne[1] in dGen[name][ligne[0]]["subject"] :
                dGen[name][ligne[0]]["subject"].append(ligne[1])
 
    return dGen


def parse_all(directory, dico, eval, id) :
    path = os.listdir(directory)

    for file in path :
        parse_blast(directory, file, dico, eval, id)


dico = {}
dico["name"] = []
#parse_blast(directory, "Shigella_sonnei_ss046-vs-Shigella_sonnei_ss046.txt", dico, 1e-60, 50)
parse_all(directory, dico, 1e-60, 50)
#parse_blast(input, dico, 1e-60, 50)
print(len(dico["name"]))


#path = os.listdir(directory) 
#for file in path :
#    besthit(directory, file) # Cree autant de fichiers .txt qu'il y a de fichiers blast

#os.system("mv *.txt output/") # Deplacer les outputs de besthit() dans un repertoire
