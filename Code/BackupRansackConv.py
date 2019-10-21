##################################En tete########################################################
#           Mis à jour
#       14/08/19 : recherche de numéros de série individuel - JL
#       04/10/19: tri des logs par dossiers au nom du num série - JL
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
RepRacine = r"C:\Users\jlaqueyr\Documents\MyNoteBook"
Nom_Ransack = "AgentRansack.exe"
MaxTentative = 3
NbrTentative = 0
Retour = 0
NouveauxChemin = ""
################################Fonction#########################################################
Liste = pyperclip.paste()

if "\r\n" in Liste:
    if Liste:
        Liste = Liste.split("\r\n")
        Liste = [x.strip() for x in Liste][:-1]
        for Sn in Liste:
            ChaineRansack = ChaineRansack+"*{}*;".format(Sn)
            ListeSn.append(Sn)
    else:
        print("Rien à convertir")
        input("Presser une touche pour sortir...")
        exit()
else:
    if Liste:
        ChaineRansack = "*{}*".format(Liste)
    else:
        print("Rien à convertir")
        input("Presser une touche pour sortir...")
        exit()

pyperclip.copy(ChaineRansack[:-1])

cmd = "{0} {1} -o \"{3}\"  -ofc -f \"{2}\" ".format(
    CheminRansack, SavedSearch, ChaineRansack, OutputDir)
print("Recherche des caractères suivant : {}".format(ChaineRansack))

Retour = subprocess.run(cmd, shell=True)
print("Recherche en cours")

for Dir in ListeSn:
    CheminDir = "{}\{}".format(RepRacine, Dir)

    if not path.exists(CheminDir):
        try:
            makedirs(CheminDir, 0o700)
        except FileExistsError:
            print("Dossier existe déjà")

with open(OutputDir) as Resultatrecherche:
    ContenuFichier = csv.reader(Resultatrecherche, delimiter=',')

    for Index, Ligne in enumerate(ContenuFichier):
        if Index == 0:
            # erreur de ransack à la première ligne : il ajoute des 3 symboles
            CheminFichier = Ligne[0][3:]+Ligne[1]
            print(CheminFichier)
        else:
            CheminFichier = Ligne[0]+Ligne[1]

        if path.isfile(CheminFichier):
            breakpoint()

            for Sn in ListeSn:
                if Sn in CheminFichier:
                    while NbrTentative < MaxTentative:
                        try:
                            NouveauxChemin = "{}\{}".format(RepRacine, Sn)
                            copy(CheminFichier, NouveauxChemin)
                            NbrTentative = MaxTentative
                        except IOError as e:
                            print("Impossible de copier le fichier. %s" % e)
                            NbrTentative += 1
                        except:
                            print("Erreur inatendu:", sys.exc_info())
                            NbrTentative += 1
                    NbrTentative = 0
                else:
                    break
                NbrTentative = 0
        else:
            print("nok")

print("Recherche fini")
input("Presser une touche pour sortir...")
remove(OutputDir)

# tester cette fonction : nom des paramètre en anglais
for proc in psutil.process_iter(attrs=['pid', 'name']):
    if Nom_Ransack in proc.info['name']:
        breakpoint()
        proc.kill()

ChaineRansack = ""

exit()

from os
