##################################En tete############################################################
#           Mis à jour
#       14/08/19 : recherche de numéros de série individuel - JL
#
##################################Lib############################################################
import pyperclip
from os import system, getcwd, path, makedirs, remove
import subprocess
import csv
from shutil import copy
from sys import exit
import psutil
#################################Variables#######################################################
Liste = ""
ListeSn = []
ChaineRansack = ""
SavedSearch = r"C:\Users\jlaqueyr\Documents\AgentRansack\CritereC62.srf"
OutputDir = getcwd()+"\RansackResultat.csv"
CheminRansack = "\"C:\Program Files\Mythicsoft\Agent Ransack\AgentRansack.exe\""
ChaineRansack = ""
RepRacine =r"C:\Users\jlaqueyr\Documents\MyNoteBook"
Nom_Ransack = "AgentRansack.exe"
###############################Fonction#########################################################
Liste = pyperclip.paste()

if "\r\n" in Liste:
    breakpoint()
    if Liste:
        Liste = Liste.split("\r\n")
        Liste = [x.strip() for x in Liste][:-1]
        for Sn in Liste :
            ChaineRansack = ChaineRansack+"*{}*;".format(Sn)    
            ListeSn.append(Sn)
        
        pyperclip.copy(ChaineRansack[:-1])
    
    else:
        print("rien à convertir")
else:
    breakpoint()
    if Liste:
        ChaineRansack = "*{}*".format(Liste) 
    else:
        print("Chaine vide")
        input("Presser une touche pour sortir...")
        exit()

cmd = "{0} {1} -o \"{3}\"  -ofc -f \"{2}\" ".format(CheminRansack, SavedSearch, ChaineRansack, OutputDir)
print("Recherche des caractères suivant : {}".format(ChaineRansack))

Retour = subprocess.run(cmd, shell=True)
print("Recherche en cours")

try:
    
    for Dir in ListeSn:
        CheminDir = "{}\{}".format(RepRacine,Dir)
        breakpoint()
        makedirs(CheminDir)

except FileExistsError:
    print("Dossier existe déjà")
    
with open(OutputDir) as Resultatrecherche:
    ContenuFichier = csv.reader(Resultatrecherche,delimiter=',')
    
    for Index,Ligne in enumerate(ContenuFichier):
        if Index ==0:
            #erreur de ransack à la première ligne : il ajoute des 3 symboles 
            CheminFichier = Ligne[0][3:]+Ligne[1]
            print(CheminFichier)
        else:
            CheminFichier = Ligne[0]+Ligne[1]

        if path.isfile(CheminFichier):
            breakpoint()

            for Sn in ListeSn:
                if Sn in CheminFichier:
                    try:
                        NouveauxChemin = "{}\{}".format(RepRacine,Sn)
                        copy(CheminFichier, NouveauxChemin)
                    except IOError as e:
                        print("Impossible de copier le fichier. %s" % e)
                    except:
                        print("Erreur innatendu:", sys.exc_info())
                else:
                   break 
        else:
            print("nok")

print("recherche fini")
input("Presser une touche pour sortir...")
remove(OutputDir)

for proc in psutil.process_iter(attrs=['pid', 'name']):
    if Nom_Ransack in proc.info['name']:
        breakpoint()
        proc.kill()

ChaineRansack=""

exit()
