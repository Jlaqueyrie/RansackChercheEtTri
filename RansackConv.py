import pyperclip
import subprocess
import csv
import psutil
from shutil import copy
from os import getcwd, path, makedirs, remove
from consolemenu import SelectionMenu
import xlsxwriter
import ctypes
ctypes.windll.kernel32.SetConsoleTitleW("Recherche de logs")

workbook = xlsxwriter.Workbook('Example2.xlsx')
worksheet = workbook.add_worksheet()
row = 0
column = 0

"""Variable"""
lst = ""
nvxChn = ""
sn = ""
strRansack = ""
lstsn = []
lstFichierTrouve = []
numCrit = 0
maxTentative = 3
retour = 0
inputNok = True

fichierResultat = getcwd() + r"\RansackResultat.csv"
chnRansack = r"C:\Program Files\Mythicsoft\Agent Ransack\AgentRansack.exe"
repRacine = r"C:\Users\jlaqueyr\Documents\ResultatRechercheRansack"

savedSearch = [r"C:\Users\jlaqueyr\Documents\AgentRansack\CritereC62.srf",
               r"C:\Users\jlaqueyr\Documents\AgentRansack\CritereEqUft.srf",
               r"C:\Users\jlaqueyr\Documents\AgentRansack\CriteriaTest.srf"]
lstProduit = ['VCM', 'EQUALIZER', 'test']

PROCNAME = "AgentRansack.exe"

"""Fonction"""


def copyFichier(chnInitial, repRacine, nomRecherche, numSerie, mTentative):
    """
    Entrée :
    Chemin initial = Chemin du fichier initial

    RepFinal = chemin destination final
    numSerie = Nom du dossier pour trier les fichiers de logs par
    num série
    mTentative = nombre maximum de tentatives pour les copies de fichier

    Sortie:
    ret = Ce finit par 0 si il y a un erreur de copie, ce finit par 1 si pas de
    d'erreur
    """

    nomFichier = path.basename(chnInitial)

    nTentative = 0
    ret = 0

    while nTentative <= mTentative or ret == 1:

        try:

            nvxChn = r"{}\{}\{}".format(repRacine,
                                                nomRecherche,
                                                numSerie,
                                                nomFichier)
            #breakpoint()
            copy(chnFichier, nvxChn)
            nTentative = mTentative
            ret = 1
            break
        except IOError:
            print("Impossible de copier le fichier. ")
            nTentative = nTentative + 1
            ret = 0

    return ret, nvxChn


def creeDossier(repRacine, nomRecherche, numSerie):
    """
    Entrée :
    RepFinal = chemin destination final
    numSerie = Nom du dossier pour trier les fichiers de logs par
    num série
    Sortie :
    ret = renvoie 1 si pas d'erreur lors d ela création de dossier et
    si une erreur
    """
    ret = 0
    chnDir = r"{}\{}\{}\\".format(repRacine, nomRecherche, numSerie)

    if not path.exists(chnDir):
        try:
            makedirs(chnDir, 0o700)
            ret = 1
        except BaseException:
            print("une erreur c'est produite")
            ret = 0
    else:
        ret = 1
    return ret


def quelType(nomProduit, cheminFichier):
    """
    Entrée :
        nomProduit : permet d'avoir différent moyen de reconnaissance des
        fichier
        cheminFichier : chemin menant au fichier à tester
    Sortie:
        resultat : dictionnaire contenant le numéros de série, type de fichier,
        type testeur
    """
    resultat = {}
    tTesteur = ''

    with open(cheminFichier, 'r') as objFichier:
        contenuFichier = objFichier.readlines()

    if nomProduit == 'vcm':
        if 'L24' in contenuFichier[0]:
            tFichier = 'RES'
            if 'UFT' in contenuFichier[0]:
                tTesteur = 'UFT'
            elif 'TSDS' in contenuFichier[0]:
                tTesteur = 'TSDS'
            elif 'VCM_T' in contenuFichier[0]:
                tTesteur = 'CADS'
            else:
                print('type de fichier inconnu')
        else:
            tFichier = 'LOG'
            if 'Equipement Ref. :' in contenuFichier[3]:
                tTesteur = 'UFT'
            elif 'Starting process with SFC:' in contenuFichier[0]:
                tTesteur = 'CADS'
            elif 'TSDS' in contenuFichier[0]:
                tTesteur = 'TSDS'
            else:
                print('fichier inconnu')

        resultat = {'typeFichier': tFichier,
                    'typeTesteur': tTesteur}

    else:
        print('test absent pour ce produit')

    return resultat


menu = SelectionMenu(lstProduit, "Select an option")
menu.show()
numCrit = menu.selected_option

#option exit du menu
if numCrit == len(lstProduit):

    exit()

else:

    print('lancer une recherche pour \
        les produits de type : {}'.format(lstProduit[numCrit]))

    input('Presser une touche')

    # MAIN PROGRAM
    lst = pyperclip.paste()

    if lst:

        if "\r\n" in lst:
            lst = lst.split("\r\n")
            lst = [x.strip() for x in lst][:-1]

            for Sn in lst:
                strRansack = strRansack + "*{}*;".format(Sn)
                lstsn.append(Sn)
        else:
            strRansack = "*{}*".format(lst)

    else:
        print('aucun caractère à rechercher')
        input("presser une touche pour sortir")
        exit()

    #Pyperclip.copy(chnransack[:-1])

    cmd = "\"{0}\" {1} -o \"{3}\"  -ofc -f \"{2}\" ".format(chnRansack, savedSearch[numCrit], strRansack, fichierResultat)

    print("recherche des caractères suivants : {}".format(strRansack))

    retour = subprocess.run(cmd, shell=True)
    print("recherche en cours patienter")

    nomRecherche = ''
    nomRecherche = input('entrée un nom pour la recherche')

    with open(fichierResultat) as rsltRecherche:
        contenuFichier = csv.reader(rsltRecherche, delimiter=',')
        contenuFichier = list(contenuFichier)

    if len(contenuFichier) >= 1:

        for Index, Ligne in enumerate(contenuFichier):
            infoFichier = {}
            if Index == 0:
                """erreur de ransack à la première ligne :
                il ajoutes 3 symboles"""
                chnFichier = Ligne[0][3:] + Ligne[1]
            else:
                chnFichier = Ligne[0] + Ligne[1]

            if path.isfile(chnFichier):

                for sn in lstsn:
                    retourDossier = 0
                    retourCopie = 0

                    if sn in chnFichier:
                        # breakpoint()
                        retourDossier = creeDossier(repRacine, nomRecherche, sn)
                        if retourDossier:
                            retourCopie, cheminFcihier = copyFichier(
                                chnFichier, repRacine, nomRecherche, sn, maxTentative)
                            if retourCopie:
                                infoFichier = quelType('vcm', chnFichier)
                                infoFichier['numSerie'] = sn
                                lstFichierTrouve.append(infoFichier)
                                break
                            else:
                                print(
                                    "Erreur lors de la copie fichier \
                                    pour le SN :{}" .format(sn))
                        else:
                            print("Erreur lors de la création du dossier" .format(sn))

            else:
                print("Le fichier {} n'existe plus".format(chnFichier))

    else:
        print("Pas de résultat dans le fichier de recherche")

    print("Recherche fini")
    input("Presser une touche pour sortir...")
    remove(fichierResultat)

    # tester cette fonction : nom des paramètre en anglais

    for proc in psutil.process_iter():
        # check whether the process name matches
        if proc.name() == PROCNAME:
            proc.kill()

    strRansack = ""
    print(lstFichierTrouve)
    input()
    #exit()
