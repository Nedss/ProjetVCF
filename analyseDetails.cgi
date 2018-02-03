#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###############################################################################
#                           IMPORT ET EN-TÊTE                                 #
###############################################################################

from statistics import mean 
import os, re, cgi, cgitb


print("""Content-type: text/html

""")

###############################################################################
#                                   FONCTIONS                                 #
###############################################################################

def ouverture(fic) :
	fichier = open(fic, 'r')
	listeFichier = []
				#On lit les lignes du fichier : si cest une ligne header on print
				#On met les lignes du fichier dans la liste
	for ligne in fichier.readlines() :
		listeFichier.append(ligne)

	fichier.close()

	return listeFichier

def extractionDico(liste):
	dico_vcf={}
	for lines in liste:
		#Recherche du header
		if re.search("^#", lines):
			continue
		#Récupération des infos importantes du VCF
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
	

		#creation du dictionnaire
		if chrm in dico_vcf :
			dico_vcf[chrm][pos]=[qual, longueur]

		else :
			dico_vcf[chrm]={pos:[qual, longueur]}

	return dico_vcf

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

def MEISurUnChromo(dico_vcf, chromo) :
	comptageMEI=0
	for pos_chr in dico_vcf[chromo]:
			comptageMEI+=1
	return comptageMEI

def affichageTailleEtContenu(dico_vcf, chromo) :
	for pos in dico_vcf[chromo] :
		print('<li> Le MEI a la position ',pos,' a une qualit&eacute; &eacute;gale a ',dico_vcf[chromo][pos][0],
			' et une taille &eacute;gale a ',dico_vcf[chromo][pos][1], '</li>')

###############################################################################
#       RECUPERATION DES DONNEES DU FORMULAIRE ET OUVERTURE DU FICHIER        #
###############################################################################

formulaire = cgi.FieldStorage()
fichier = formulaire["recupFichier"].value
listeFichier = ouverture(fichier)
dico_vcf = extractionDico(listeFichier)
recupChromo = formulaire['chromo'].value

###############################################################################
#                           AFFICHAGE DE LA PAGE                              #
###############################################################################

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
		    	<form action='analyseVCF.cgi' method='POST'>
				<section id='saisieFichier'>
					<input type='submit' name='envoyer' value='recommencer avec un autre fichier'>
					<input type='hidden'>
				</section>
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

				<script src='../js/analyseVCF.js'></script>

				<h4>Informations sur le chromosome 
	""")

print("<em>",recupChromo,"</em> :")

print("""
				</h4>

			<h6 style="text-align:center; text-decoration:underline;">Nombre de MEI : 

	""")

#Calcul du nombre de MEI sur le chromosome
nbMEI = MEISurUnChromo(dico_vcf, recupChromo)
print(nbMEI,"</h6>")
print("""
	<div class=divDetails>
		<ul>""")

affichageTailleEtContenu(dico_vcf, recupChromo)
print("</ul>")


print("""
				</section>
			</form>

		</main>
		<footer>
			Projet sur l'analyse VCF r&eacute;alise par Moussa Samb, Nicolas Soirat et Axelle Nicolas, <em>Master Bioinformatique, Connaissances et Donn&eacute;es</em>
		</footer>
	</body>
</html>

		""")
