#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###############################################################################
#                                 IMPORT ET EN-TÊTE                           #
###############################################################################

from statistics import mean 
import os, re, cgi, cgitb

print("""Content-type: text/html

""")

###############################################################################
#                                  FONCTIONS                                  #
###############################################################################

def verificationFichier(saisieFichier) :
	tabExtraction = saisieFichier.split(".")
	verif = ''
	try :
		if tabExtraction[1] == 'vcf' and os.path.exists(saisieFichier) : #Si le fichier est un vcf et qu'il existe, OK
			verif='VCF'
		else :
			verif = 'NonVCF'
	except :
		print("<h3>Vous n'avez pas saisi de fichier ...</h3>")
		verif='pasFichier'

	return verif


def ouverture() :
	fichier = open(formulaire["saisie"].value, 'r')
	listeFichier = []
#On met les lignes du fichier dans la liste
	for ligne in fichier.readlines() :
		listeFichier.append(ligne)
	verif = 'VCF'
#on ferme le fichier
	fichier.close()

	return listeFichier


def verificationContenu(listeFichier) :
	listeVerifs=[]
	verifVersion =false
	verifHeader =true
	verifDonnees=true
	for ligne in listeFichier :
#---------------------1 => Verification de la version (VERSION 4)-----------------------
		ligneVersion = re.search("#.*fileformat=VCF", ligne)
		if ligneVersion : #Si c'est la ligne version
			version = re.search("#.*VCFv4\.[0-9]", ligne)
			if version : 
				verifVersion = true
				listeVerifs.append(verifVersion)
#---------------------2 => Verification du header-----------------------
	listeHeader = extractionHeader(listeFichier)
	if len(listeHeader) < 10 :
		verifHeader = false
		listeVerifs.append(verifHeader)
#---------------------2 => verification des Donnees-----------------------
	listeDonnees = extractionDico(listeFichier)
	if len(listeDonnees) < 30 :
		verifDonnees = false
		listeVerifs.append(verifDonnees)

	return listeVerifs

def extractionHeader(liste):
	list_header=[]
	for lines in liste:
		#Recherche du header
		if re.search("^#", lines):
			list_header.append(lines)
	return list_header

def affichageHeader(liste_header):
	print("<textarea>")
	for i in liste_header :
		print(i)
	print("</textarea>")

def extractionDico(liste):
	dico_vcf={}
	for lines in liste:
		#Recherche du header
		if re.search("^#", lines):
			continue
		#Recuperation des infos importantes du VCF (numero du chromo, la position, la qualite du MEI et sa longueur)
		else:
			tab=lines.split("\t")
			chrm=tab[0]
			pos=tab[1]
			qual=tab[5]
			longueur_temp=tab[7]
			longueur=''
			if re.search("^SVLEN", longueur_temp):
				# On recherche si la longueur est présente dans le VCF
				longueur_split=longueur_temp.split(";")[0]
				# Si on trouve la longueur on split la colonne sur ; qui représente les différentes valeurs 
				longueur=longueur_split.split("=")[1]
				# On split ensuite sur "=" pour n'obtenir que la valeur souhaitée 
			else:
				# Si la longueur n'est pas renseignée on l'indique
				longueur="inconnue"
	

		#Création du dictionnaire
		if chrm in dico_vcf :
			dico_vcf[chrm][pos]=[qual, longueur]

		else :
			dico_vcf[chrm]={pos:[qual, longueur]}

	return dico_vcf

def affichageCompletDico(dico_vcf):
	for name_chr in dico_vcf :
		for pos_chr in dico_vcf[name_chr]:
			print("numero du chromosome : ",name_chr,"position : ",pos_chr,"qualite : ",
			dico_vcf[name_chr][pos_chr][0], "taille : ",dico_vcf[name_chr][pos_chr][1])

def affichageDico(dico_vcf):
	for name_chr in dico_vcf :
		if name_chr == 1 :
			#On choisi par defaut le chromo 1 dans la liste deroulante
			print("<option selected='select'>", name_chr, "</option>")
		else :
			print("<option>", name_chr, "</option>")


def statDico(dico_vcf):
	#On trouve combien il y a d'élements par chromosomes 
	mei=[]
	#On stocke le numÉro des chromosomes pour que le nombre de MEI dans le dico_vcf soit apparenté au bon chromosome
	statMEI={"1":[], "2":0, "3":0, "4":0, "5":0, "6":0, "7":0, "8":0, "9":0, "10":0,
	"11":0, "12":0, "13":0, "14":0, "15":0, "16":0, "17":0, "18":0, "19":0, "20":0, "21":0, "22":0, 'X':0, 'Y':0}
	for name_chr in dico_vcf:
		res=0
		for chromoMEI in statMEI:
			if name_chr!=chromoMEI:
				continue
			else:
				for pos_chr in dico_vcf[name_chr]:
					res+=1
				statMEI[chromoMEI]=res
	#Liste du nombre de MEI par chromosomes (croissant)
	nombreMEI=[]
	for chromoMEI in statMEI:
		nombreMEI.append(statMEI[chromoMEI])
	#Calcul moyenne, min et max
	moyenne=mean(nombreMEI)
	maximum=max(nombreMEI)
	minimum=min(nombreMEI)
	chromoMax=""
	chromoMin=""

	#Appariement chromosome et le MEI le plus grand (ou le moins grand)
	for chromoMEI in statMEI:
		if statMEI[chromoMEI]!=maximum:
			continue
		else :
			chromoMax=chromoMEI

	for chromoMEI in statMEI:
		if statMEI[chromoMEI] != minimum:
			continue
		else :
			chromoMin=chromoMEI

	return statMEI, moyenne, chromoMax, maximum, chromoMin, minimum

def moyenneMEI(mei) :
	#Calcul de la moyenne à partir dela fonction mean 
	#La fonction a été importé à partir de statistic
	moyenne=mean(mei)
	return moyenne

def maxChromo(mei):
	#Recherche du maximum 
	rech_max=0
	for m in range(0, len(mei)):
		if mei[m]>rech_max:
			rech_max=mei[m]
			m_max=m+1 
			#Vu que notre nombre de MEI est trié dans l'endroit, en commançant par le chromosome 1
			# on sait que m+1 correspond au chromosome que l'on cherche (m commençant à 0 il n'y 
			# a pas de chromosome 0). 
	return rech_max, m_max


def minChromo(mei):
	#Recherche du maximum 
	rech_min=mei[0]
	for m in range(1, len(mei)):
		if mei[m]<rech_min :
			rech_min=mei[m]
			m_min=m+1 
	return rech_min, m_min

###############################################################################
#                    RECUPERATION DES DONNEES DU FORMULAIRE                   #
###############################################################################

formulaire = cgi.FieldStorage()

#Initialisation de la saisie
saisieFichier = ''

###############################################################################
#                               AFFICHAGE DE LA PAGE                          #
###############################################################################

#Si la saisie est vide ou que l'utilisateur n'a pas cliqué sur envoyer => page de base avec que la saisie + message d'erreur
if "saisie" not in formulaire or "envoyer" not in formulaire or verificationFichier(formulaire["saisie"].value) == 'pasFichier' :
	print("""
	<!DOCTYPE html>
	<html>
	  <head>
	    <meta charset='UTF-8'>
	    <title>Projet vcf</title>
	    <link rel='stylesheet' href='../css/analyseVCF.css'>
	    <link rel='stylesheet' href='../font/css/font-awesome.css'>
		<link href="https://fonts.googleapis.com/css?family=Acme|Work+Sans" rel="stylesheet"> 
	  </head>
	  <body>
	  	<header>
	    	<h1>Analyse VCF</h1>
	    </header>
	    <main>
	    	<form class='form1' action='analyseVCF.cgi' method='POST'>
				<section id='saisieFichier'>
					<label>Entrez le fichier :</label>
					<input type='text' name='saisie'>
					<input type='submit' name='envoyer'>
				</section>
			</form>
		</main>
		<style>
		#foot{position: absolute;bottom:0;right:0;}
		</style>
		<footer id='foot'>
			Projet sur l'analyse VCF r&eacute;alise par Moussa Samb, Nicolas Soirat et Axelle Nicolas, <em>Master Bioinformatique, Connaissances et Donn&eacute;es</em>
		</footer>
	  </body>
	</html>
	""")

#Si la saisie est un "fichier" (si il y a un point) mais que ce n'est pas un vcf ou que le fichier n existe pas => page de base avec que la saisie + message d'erreur
elif verificationFichier(formulaire["saisie"].value) == 'NonVCF' :
		print("""
		<!DOCTYPE html>
		<html>
		  <head>
		    <meta charset='UTF-8'>
		    <title>Projet vcf</title>
		    <link rel='stylesheet' href='../css/analyseVCF.css'>
		    <link rel='stylesheet' href='../font/css/font-awesome.css'>
			<link href="https://fonts.googleapis.com/css?family=Acme|Work+Sans" rel="stylesheet"> 
		  </head>
		  <body>
		  	<header>
		    	<h1>Analyse VCF</h1>
		    </header>
		    <main>
		    	<form class='form1' action='analyseVCF.cgi' method='POST'>
					<section id='saisieFichier'>
						<label>Entrez le fichier :</label>
						<input type='text' name='saisie'>
						<input type='submit' name='envoyer'>
					</section>
				</form>
				<h3>Le fichier que vous avez saisi n'existe pas ou n'est pas un VCF</h3>
			</main>
			<style>
			#foot{position: absolute;bottom:0;right:0;}
			</style>
			<footer id='foot'>
				Projet sur l'analyse VCF r&eacute;alise par Moussa Samb, Nicolas Soirat et Axelle Nicolas, <em>Master Bioinformatique, Connaissances et Donn&eacute;es</em>
			</footer>
		  </body>
		</html>
		""")

#Si la saisie est un VCF qui existe => page complete avec les infos generales
else : 
	#Ouverture du fichier, transfert des données du fichier dans la liste et fermeture du fichier
	listeFichier = ouverture()
	#On met dans le dico les données vcf
	dico_vcf= extractionDico(listeFichier)
	#On extrait les stats
	dicoChromoMei, moyenne, chromoMax, maximum, chromoMin, minimum = statDico(dico_vcf)
	#Récupération du fichier dans un input type hidden pour pouvoir le transmettre à la page analyseDetails via le formulaire 
	recupFichier = formulaire["saisie"].value
	

	print("""
		<!DOCTYPE html>
		<html>
		  <head>
		    <meta charset='UTF-8'>
		    <title>Projet vcf</title>
		    <link rel='stylesheet' href='../css/analyseVCF.css'>
		    <link rel='stylesheet' href='../font/css/font-awesome.css'>
		  </head>
		  <body>
		    <header>
		    	<h1>Analyse VCF</h1>
		    </header>
		    <main>
		    	<form class='form1' action='analyseVCF.cgi' method='POST'>
					<section id='saisieFichier'>
							<input type='submit' name='envoyer' value='recommencer avec un autre fichier'>		
					</section>

				<h2>Donn&eacute;es de votre fichier :</h2>
				<section id='donneesHeader'>
					<div class='description'>
						<h3>Header
							<a class='plus-toggle' href='#'>
								<i class='fa fa-plus' aria-hidden='true'></i>
							</a>
						</h3>
		<!-- quand on clique sur licone -, la div se cache via la classe hide -->
						<div class='hide'> 
							
			
	""")	
	#Affichage du header dans la div
	affichageHeader(extractionHeader(listeFichier))
	print("""
						</div>
					</div>
				</section>

				<section id='Statistiques'>
					<h4>Les statistiques de votre &eacute;chantillon 
	""") 

	#On affiche le nombre de chromosomes dans l'échantillon (-1 X et Y)
	print("(",len(dico_vcf)-1,"chromosomes ) <br><em>- toutes les qualit&eacute;s sont accept&eacute;es -</em></h4>") 

	print("""
					<div id="blocsStat">
						<div><h5>MOYENNE G&Eacute;N&Eacute;RALE</h5>
	""")

	#on affiche la moyenne generale (on tronque le resultat avec int(value))
	print("<p>On trouve en moyenne ",int(moyenne)," MEI par chromosome (moyenne tronqu&eacute;e) </p></div>")

	print("""
						<div id="milieu"><h5>MAXIMUM</h5>
	""")

	#Affichage chromo avec le plus de MEI
	print("<p>Le chromosome ",chromoMax," contient le plus de MEI (avec ",maximum," MEI)</p></div>")

	print("""
						<div><h5>MINIMUM</h5>
	""")

	#Affichage chromo avec le moins de MEI
	print("<p>Le chromosome ",chromoMin," contient le moins de MEI (avec ",minimum," MEI)</p></div>")

	print("""
					</div>
					<div style='margin-top:3em;'><h5>NOMBRE DE MEI PAR CHROMOSOME</h5>
					<div class=divDetails>
						<ul id='ulDetails'>
	""")

	#On récupère les clés et les valeurs du dico donc les numéros des chromos et le nombre de MEI
	for numChromo, nbMEI in dicoChromoMei.items() :
		print("<li> Le chromosome ",numChromo,"contient ",nbMEI, " MEIs </li>")

	print("""
						</ul>
						</div>
			
	""")	

	print("""
					</div>

					<h4>Encore plus de d&eacute;tails</h4>
					<p>Pour plus d'informations, choisir un chromosome : </p>
				</form>
			</section>
			<form id='form2' action='analyseDetails.cgi' method='POST'>
				<select name='chromo' id='chromo'>
	""")

	#Affiche dans les balises option les chromosomes dans la liste deroulante
	numeroChromo = affichageDico(dico_vcf)

	print("</select><input type='hidden' name='recupFichier' value=",recupFichier,">")
	print("""
				<input type='submit' name='soumettre' id='soumettre' value='Je choisis ce chromosome'>	
			</form>
			<script src='../js/analyseVCF.js'></script>
		</main>
		<footer>
			Projet sur l'analyse VCF r&eacute;alise par Moussa, Nicolas et Axelle Nicolas, <em>Master Bioinformatique, Connaissances et Donn&eacute;es</em>
		</footer>
	</body>
</html>
	""")



