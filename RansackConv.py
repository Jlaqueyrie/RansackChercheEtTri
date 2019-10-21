import pyperclip
import subprocess
import csv
import psutil
from shutil import copy
from os import getcwd, path, makedirs, remove

"""Variable"""
Liste = ""
ListeSn = []
ChaineRansack = ""
SavedSearch = r"C:\Users\jlaqueyr\Documents\AgentRansack\CritereC62.srf"
FichierResultat = getcwd() + r"\RansackResultat.csv"
CheminRansack = r"C:\Program Files\Mythicsoft\Agent Ransack\AgentRansack.exe"
ChaineRansack = ""
RepRacine = r"C:\Users\jlaqueyr\Documents\ResultatRechercheRansack"
Nom_Ransack = "AgentRansack.exe"
MaxTentative = 3
NbrTentative = 0
Retour = 0
NouveauxChemin = ""
Sn = ""

"""Fonction"""


def CopyFichier(CheminInitial, RepFinal, NumSerie, MTentative):
    """
    Entrée :
    Chemin initial = Chemin du fichier initial
    RepFinal = chemin destination final
    NumSerie = Nom du dossier pour trier les fichiers de logs par
    num série
    MTentative = nombre maximum de tentatives pour les copies de fichier

    Sortie:
    Ret = Ce finit par 0 si il y a un erreur de copie, ce finit par 1 si pas de
    d'erreur
    """

    NomFichier = path.basename(CheminInitial)

    NTentative = 0
    Ret = 0

    while NTentative <= MTentative or Ret==1:

        try:
                
            NouveauxChemin = r"{}\{}\{}".format(RepRacine,
                                                NumSerie,
                                                NomFichier)                        
            copy(CheminFichier, NouveauxChemin)
            NTentative = MTentative
            Ret = 1
            break
        except IOError:
            print("Impossible de copier le fichier. ")
            NTentative = NTentative+1
            Ret = 0

    return Ret


def CreeDossier(RepRacine, NumSerie):
    """
    Entrée :
    RepFinal = chemin destination final
    NumSerie = Nom du dossier pour trier les fichiers de logs par
    num série
    Sortie :
    Ret = renvoie 1 si pas d'erreur lors d ela création de dossier et
    si une erreur
    """
    Ret = 0
    CheminDir = r"{}\{}".format(RepRacine, NumSerie)

    if not path.exists(CheminDir):
        try:
            makedirs(CheminDir, 0o700)
            Ret = 1
        except :
            print("une erreur c'est produite")
            Ret = 0
    else:
        Ret = 1
    return Ret


# main program
Liste = pyperclip.paste()
if Liste:

    if "\r\n" in Liste:

        Liste = Liste.split("\r\n")
        Liste = [x.strip() for x in Liste][:-1]

        for Sn in Liste:
            ChaineRansack = ChaineRansack + "*{}*;".format(Sn)
            ListeSn.append(Sn)
    else:

        ChaineRansack = "*{}*".format(Liste)
else:

    print("Rien à convertir")
    input("Presser une touche pour sortir...")
    exit()

pyperclip.copy(ChaineRansack[:-1])

cmd = "\"{0}\" {1} -o \"{3}\"  -ofc -f \"{2}\" ".format(
    CheminRansack, SavedSearch, ChaineRansack, FichierResultat)

print("Recherche des caractères suivant : {}".format(ChaineRansack))

Retour = subprocess.run(cmd, shell=True)
print("Recherche en cours")


with open(FichierResultat) as Resultatrecherche:
    ContenuFichier = csv.reader(Resultatrecherche, delimiter=',')
    ContenuFichier = list(ContenuFichier)

if len(ContenuFichier) > 1:

    for Index, Ligne in enumerate(ContenuFichier):
        if Index == 0:
            """erreur de ransack à la première ligne :
            il ajoute des 3 symboles"""
            CheminFichier = Ligne[0][3:] + Ligne[1]
        else:
            CheminFichier = Ligne[0] + Ligne[1]

        if path.isfile(CheminFichier):

            for Sn in ListeSn:
                RetourDossier = 0
                RetourCopie = 0

                if Sn in CheminFichier:
                    #breakpoint()
                    RetourDossier = CreeDossier(RepRacine, Sn)
                    if RetourDossier:
                        RetourCopie = CopyFichier(CheminFichier, RepRacine, Sn,
                                                  MaxTentative)
                        if RetourCopie:
                            break
                        else:
                            print("Erreur lors de la copie fichier pour le SN :{}"
                                  .format(Sn))
                    else:
                        print("Erreur lors de la création du \
                              dossier" .format(Sn))
                Sn = ""

        else:
            print("Le fichier {} n'existe \
                  plus".format(path.basename(CheminFichier)))

else:
    print("Pas de résultat dans le fichier de recherche")

print("Recherche fini")
input("Presser une touche pour sortir...")
remove(FichierResultat)

# tester cette fonction : nom des paramètre en anglais
for proc in psutil.process_iter(attrs=['pid', 'name']):
    if Nom_Ransack in proc.info['name']:
        proc.kill()

ChaineRansack = ""

exit()
