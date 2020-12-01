# python3 plagiat.py -dir blast_outputs/

import sys, os
import time

from sys import argv
from timeit import default_timer as timer
def usage():
    print("""
          obligatory:
          ==========
          -dir directory with blast results
          optionnal:
          ==========
          -eval eval value(default 1e-3)
          -cov coverage percentage(default 70)
          -id identity value(default 30)
          -out ouput file
        """)
#takes the blast results directory
if len(argv)>1:
    try:
        dir=sys.argv[sys.argv.index('-dir')+1]
    except:
        print("Err input directory missing")
        usage()
        sys.exit()
    #takes evalue treshold
    try : 
        seuil_evalue = float(sys.argv[sys.argv.index("-eval")+1])
    except:
        seuil_evalue=1e-3
        print("Default evalue = 1e-3")
    #identity treshold
    try:
        tresh_id=float(sys.argv[sys.argv.index("-id")+1])
    except:
        tresh_id=30
        print("Default id treshold = 30")
    #coverage treshold
    try:
        tresh_cov=float(sys.argv[sys.argv.index("-cov")+1])
    except:
        tresh_cov=70
        print("Default coverage value = 70")
    try:
        output=sys.argv[sys.argv.index("-out")+1]
    except:
        output="CoreGenome"
        print("Default output: CoreGenome")
else:
    usage()
    sys.exit()

def parse_blast(fichier_blast, dGen, eval, id, cov):
    """ 
    input : prend le nom d'un fichier
    output : deux listes, l'une des query, et l'autre des subject pour les meilleurs hit
    function : parse une sortie de blast
    """
    #Ouverture fichier
    file = open(dir+fichier_blast, "r")
    lines = file.readlines()
    file.close()
  
    name=fichier_blast.split("-")[0]
    
    if not name in dGen["name"]: #add the query genome name to the dictionary if it doesn't exist yet
        dGen["name"].append(name)
        dGen[name]={} 
        dGen[name]["query"]=[]
 
    ligne_hit = "hit" #flag
    cpt = 0 #Compteur de ligne

    #Browse file line by line
    for line in lines:
        if ligne_hit in line and line.split()[1]!="0": # add condition when there is not hit
            ligne_interet = lines[cpt+1] #On selectionne la ligne juste apres celle des hit pour avoir acces aux valeurs qui nous interesse
            ligne_interet = ligne_interet.split() #Separe les composants au niveau des espaces en une liste
                
            if float(ligne_interet[2])>id and float(ligne_interet[11])<eval : #condition to be added in the dict, id, eval and coverage
                if not ligne_interet[0] in dGen[name]["query"]: #check if the query is already in the dict
                    dGen[name]["query"].append(ligne_interet[0])
                    dGen[name][ligne_interet[0]]={}
                    dGen[name][ligne_interet[0]]["subject"]=[]
                    dGen[name][ligne_interet[0]]["subject"].append(ligne_interet[1])
                elif not ligne_interet[1] in dGen[name][ligne_interet[0]]["subject"]:#add the subject if not already in the dict
                    dGen[name][ligne_interet[0]]["subject"].append(ligne_interet[1])
        cpt +=1
    return dGen

def search_orthologue(dico, fout, eval, id, cov):
    """
    input : takes the dictionnary
    output : file with the core genome size and and all the related genes
    fonction : check if genes are ortholog using reciprocity
    """
    f=open(fout, "w")
    name=[]
    size=len(dico["name"])
    coreGenome=0
    for name1 in dico["name"]:
        for gene1 in dico[name1]["query"]:
            #f.write(gene1)
            count=0
            for name2 in dico["name"]:
                if name2 not in name:
                    for gene2 in dico[name2]["query"]:
                        if gene1 in dico[name2][gene2]["subject"] and gene2 in dico[name1][gene1]["subject"]:
                            #f.write("\t"+gene2)
                            count+=1
            if count==size:
                coreGenome+=1
                #print(coreGenome)
                #f.write("\t"+str(count))

            #f.write("\n")
        name.append(name1)
    f.write("e-val treshold = "+str(eval)+"\tid treshold = "+str(id)+"\tcoverage percentage treshold = "+str(cov)+"\n")
    f.write("Core genome = "+str(coreGenome))
    f.close()

def parseAll(dir, dico, eval, id, cov):
    """
    input: directory with blast results
    output: dictionnary
    function:
    """
    path=os.listdir(dir)
    for file in path:
        parse_blast(file, dico, eval, id, cov)

def core_genome(dir, eval, id, cov, fout):
    dico={}
    dico["name"]=[]

    #time traceback
    begin = time.time()
    parseAll(dir, dico, eval, id, cov)
    end = time.time()
    print("Duree du parsing : ",end-begin,"sec")

    begin = time.time()
    search_orthologue(dico, fout, eval, id, cov)
    end = time.time()
    print("Temps de calcul core genome : ",end-begin,"sec")
"""
dGen={}
dGen["name"]=[]
parseAll(dir, dGen, seuil_evalue, tresh_id, tresh_cov)
search_orthologue(dGen, output)
"""
#core_genome(dir, seuil_evalue, tresh_id, tresh_cov, output)
start=timer()
core_genome(dir, 1e-20, 25, 80, "benchmark80")

print("time",timer()-start)
#core_genome(dir, 1e-60, 40, 80, "benchmark6")