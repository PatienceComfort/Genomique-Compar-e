#!/usr/bin/python3
"""
Author : Hugues Herrmann
Purpose : 
Date : 21/11/20
"""
# Code tres largement inspire de Thomas Rambaut
# python3 hugues_core_genome.py -dir_blast blast_outputs -dir_besthit output 

import sys, os


dir_blast = sys.argv[sys.argv.index("-dir_blast")+1]
dir_besthit = sys.argv[sys.argv.index("-dir_besthit")+1]


def besthit(directory, blast_output) :
# Parcourt un output de blast et ecrie le besthit dans un nouveau fichier output
# Input : Un fichier output_blast + le repertoire dans lequel se trouve le fichier
# Output : Un fichier .txt contenant les besthits 

    input = open(directory + "/" + blast_output, "r") # Ouvrir le fichier de resultats blast
    output = open(blast_output.split(".")[0] + ".txt", "w") # Ouvrir le fichier output portant le meme nom que le fichier input

    for ligne in input : # Pour chaque ligne du fichier

        if not ligne.startswith("#") :
            list = ligne.split("\t") # Liste des resultats du best hit
                            
            query_id = list[0]
            subject_id = list[1]
            identity = list[2]
            e_value = list[11]
            
            output.write(query_id+"\t"+subject_id +"\t"+identity+"\t"+e_value+"\t\n") # Ecrire les stats du best hit
            
    input.close()
    output.close()



def parse_blast(directory, besthit_output, dGen, eval, id) :
# Cree un dictionnaire qui contient toutes les especes, tous ses genes en "query" et le best hit du gene query en "subject"
# Input : un fichier issu de besthit(), le repertoire ou est stocke ce fichier, un dico, une pvalue et un score identite
# Output : Un dico
    file = open(directory + "/" + besthit_output, "r")
    lignes = file.readlines()
    file.close()

    name = besthit_output.split("-")[0] # Le nom de l'espece blastee

    if not name in dGen["name"] : # Liste des noms des especes
        dGen["name"].append(name)
        dGen[name] = {}
        dGen[name]["query"] = []

    for ligne in lignes :
        ligne = ligne.split()

        if float(ligne[2])>id and float(ligne[3])<eval :
            if not ligne[0] in dGen[name]["query"] :
                dGen[name]["query"].append(ligne[0])
                dGen[name][ligne[0]] = {}
                dGen[name][ligne[0]]["subject"] = []
                dGen[name][ligne[0]]["subject"].append(ligne[1])
            elif not ligne[1] in dGen[name][ligne[0]]["subject"] :
                dGen[name][ligne[0]]["subject"].append(ligne[1])

    return dGen


def parse_all(directory, dico, eval, id) :
# Parse tous les fichiers dans le directory
# Output : un dico qui contient toutes les especes, toutes les query et les besthits de chaque query
    path = os.listdir(directory)

    for file in path :
        parse_blast(directory, file, dico, eval, id)


def orthologue(dico) :
    #f = open(fout, "w")
    name = []
    size = len(dico["name"])
    coreGenome = 0

    for name1 in dico["name"] :
        for gene1 in dico[name1]["query"] :
            count = 0

            for name2 in dico["name"] :
                if name2 not in name :#pour vérifier qu'on a pas déjà testé ce couple
                    for gene2 in dico[name2]["query"] :
                        
                        if gene1 in dico[name2][gene2]["subject"] and gene2 in dico[name1][gene1]["subject"] :
                            count += 1
            if count == size :
                coreGenome += 1
                print("Core genome iteration :" + str(coreGenome))
        print(coreGenome)
        name.append(name1)
    print(coreGenome)
    #f.write("Core genome = "+str(coreGenome))
    #f.close()



#path = os.listdir(dir_blast) 
#for file in path :
#    besthit(dir_blast, file) # Cree autant de fichiers .txt qu'il y a de fichiers blast
#os.system("mkdir output")
#os.system("mv *.txt output/")


dico = {}
dico["name"] = []
parse_all(dir_besthit, dico, 1e-10, 30)
print("fin parse_all() ----------------------")
orthologue(dico)

print("---------------fin")

# 1e-60, id=60 = 541 genes
# 1e-10, id=30 = 1168
