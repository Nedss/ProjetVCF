###########################################################
#                   Analyse VCF                           #
###########################################################

Bienvenue sur le README du projet système du groupe composé d'Axelle NICOLAS, Moussa SAMB et Nicolas SOIRAT.

Le script se présente sous deux versions : 
- Un script python qui se lance sur la console (analyseVCF.py)
- Un script cgi qui se lance via un navigateur web (analyseVCF.cgi + analyseDetails.cgi)

Un fichier exe.sh encore en béta permet pour le moment d'exécuter le script python de façon sûre, mais quelques problèmes
sont recontrés du côté du CGI sur les OS Ubuntu (gestion du nom d'utilisateur dans l'url). 

Le but de ce script est de donner une vision globale du fichier VCF à un utilisateur. Pour cela le script permet de :
- Extraire le header (si l'utilisateur en a besoin ou non)
- Trouver le chromosome qui a le plus de MEI, le moins de MEI et réaliser une moyenne de MEI par chromosome, sur tout le VCF
- Avoir une vue d'ensemble sur les nombres de MEI par chromosome
- Sélectionner un chromosome qui nous intéresse et renseigner son nombre de MEI, leur longueur et leur qualité. 


Contraintes : 
--------------

- Le fichier à l'entrée doit être un fichier .vcf
- Le fichier à l'entrée doit contenir un header (>10) ainsi qu'un nombre suffisant de lignes au niveau du contenu biomoléculaire (>30)
- Les chromosomes ne disposant pas de MEI ne peuvent être sélectionnés. 
- Pour utiliser de façon optimale le script il faut que la longueur des MEI dans le VCF soit précédée de la valeur "SVLEN="
- La version du VCF doit être au delà de la 4.0. 