###############################################################################
# Titre: recherche ransack et tri résultat
# Version: 0.1
# Auteur: Jlaqueyrie
# Date : 11/09/19
# Historique:
###############################################################################

Le but du script et de récupérer une liste de numéro de série depuis le press papier 
windows, puis de lancer l'utilitaire "agent ransack" qui lui va recherché dans un ensemble de répertoire les 
logs comportant le numéro de série. 
Une fois la recherche termnié sur l'ensemble des répertoire le szcript extrait les chemin des fichier trouvés,
plus les copie dans un répertoire locale nommé avec le numéros de série de la pièce.
Le but étant de faire une recherche global des fichiers de log disponible pour une pièce donnée.