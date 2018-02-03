#!/usr/bin/env python3
#-*- coding: Utf-8 -*-

###########################################################
#                       HEAD                              #
###########################################################
from statistics import mean 
import sys, re, os
os.system("clear")

###########################################################
#                     FONCTIONS                           #
###########################################################

#__ Partie VERIFICATION DU FICHIER__#
#####################################

def cheminFichier() :
	print("Saisir le chemin du fichier :")
	saisir = input()
	return saisir


def ouvertureFichierVCF() :      
	formatVCF = False
	recommencer = 'o'
	fichier = None
	listeFichier=[]
	while formatVCF == False and recommencer == 'o' or recommencer == 'oui' :
		saisi = cheminFichier()
		tabExtraction = saisi.split(".")
		try :
			if tabExtraction[1] != 'vcf' : #Si le fichier n'est pas en format VCF
				print("Erreur saisie : votre fichier n'est pas au format vcf\nVoulez-vous ressaisir un fichier VCF ? (oui, o / non, n)")
				recommencer = input()
			elif tabExtraction[1] == 'vcf' and os.path.exists(saisi) : #Si le fichier est un VCF et qu'il existe, OK
				formatVCF = True
				fichier = open(saisi, 'r')
				print("Ouverture du fichier VCF '", saisi, "' reussie !")
				listeFichier = verificationContenu(fichier)
				break
			else:
				print("Le fichier VCF n'existe pas...\nVoulez-vous ressaisir un fichier VCF ? (oui, o / non, n) ")
				recommencer=input()
		except :
			if formatVCF == False : #Ne pas demander une autre saisie si on a deja ouvert le VCF
				print("Erreur saisie : vous n'avez pas saisi de fichier.\nVoulez-vous ressaisir un fichier VCF ? (oui, o / non, n) ")
				recommencer = input()
	return fichier, listeFichier

def verificationContenu(fichier) :
	#On lit le fichier ligne par ligne 
	#(1) tant que la ligne ne comporte pas "fileformat" 
	#(2) qu'il existe un header
	#(3) qu'il y a suffisament de donnees pour commencer
	ligneFormat = False
	#Création liste fichier pour le manipuler
	listeFichier=[]
	for ligne in fichier.readlines() :	
#---------------------1 => verification de la version (VERSION 4)-----------------------
		ligneVersion = re.search("#.*fileformat=VCF", ligne)
		if ligneVersion : #Si cest la ligne version
			version = re.search("#.*VCFv4\.[0-9]", ligne)
			if version : 
				print("Verification version : OK (4.)")
			else : 
				print("Erreur, la version du fichier est trop ancienne...\n")
				fermetureFichierVCF(fichier)
				sys.exit("FIN DU PROGRAMME !")
#---------------------AJOUT DE LA LIGNE DANS LA LISTE-----------------------
		listeFichier.append(ligne)
#---------------------2 => verification du header-----------------------
	listeHeader = extractionHeader(listeFichier)
	if len(listeHeader) < 10 :
		print("Données insuffisantes dans le header")
		fermetureFichierVCF(fichier)
		sys.exit("FIN DU PROGRAMME !")
	else :
		print("Verification header : OK")
#---------------------2 => verification des données-----------------------
	listeDonnees = extractionDico(listeFichier)
	if len(listeDonnees) < 10 :
		print("Il n'y a pas assez de données génomiques ...")
		fermetureFichierVCF(fichier)
		sys.exit("FIN DU PROGRAMME !")
	else :
		print("Verification des données génomiques : OK")

	return listeFichier


def fermetureFichierVCF(fichier) :
	if fichier :
		try :
			fichier.close()
			print("Fermeture du fichier réussie")
		except :
			print("Erreur dans l'ouverture du fichier")
			sys.exit("FIN DU PROGRAMME !")

				
#__ Partie EXTRACTION et ANALYSE des DONNEES __#
#################################################

def extractionDico(liste):
	dico_vcf={}
	for lines in liste:
		#Recherche du header
		if re.search("^#", lines):
			continue
		#Création du dictionnaire avec les infos importantes du VCF
		else:
			tab=lines.split("\t")
			chrm=tab[0]
			pos=tab[1]
			qual=tab[5]
			longueur_temp=tab[7]
			if re.search("^SVLEN", longueur_temp):
				# On recherche si la longueur est présente dans le VCF
				longueur_split=longueur_temp.split(";")[0]
				# Si on trouve la longueur on split la colonne sur ; qui représente les différentes valeurs 
				longueur=longueur_split.split("=")[1]
				# On split ensuite sur "=" pour n'obtenir que la valeur souhaitée 
			else:
				# Si la longueur n'est pas renseignée on l'indique
				longueur="Inconnue"
			if chrm in dico_vcf:
					dico_vcf[chrm][pos]=[qual, longueur]
			else:
				dico_vcf[chrm]={pos:[qual, longueur]}
	return dico_vcf

def extractionHeader(liste):
	list_header=[]
	for lines in liste:
		#Recherche du header
		if re.search("^#", lines):
			list_header.append(lines)
		#Création du dictionnaire avec les infos importantes du VCF
	return list_header


def affichageHeader(list_header):
	print("Affichage du header")
	for i in list_header:
		print(i)

def affichageDico(dico_vcf):
	print("Affichage du contenu biomoléculaire du VCF")
	for name_chr in dico_vcf :
		for pos_chr in dico_vcf[name_chr]:
			print("N°",name_chr," Position : ",pos_chr," Qual : ", dico_vcf[name_chr][pos_chr][0], " Longueur : ",dico_vcf[name_chr][pos_chr][1])


def statDico(dico_vcf):
	#On trouve combien il y a d'élements par chromosomes 
	statMEI={"1":[], "2":0, "3":0, "4":0, "5":0, "6":0, "7":0, "8":0, "9":0, "10":0, "11":0, "12":0, "13":0, "14":0, "15":0, "16":0, "17":0, "18":0, "19":0, "20":0, "21":0, "22":0, 'X':0, 'Y':0}
	for name_chr in dico_vcf:
		res=0
		for chromoMEI in statMEI:
			if name_chr!=chromoMEI:
				continue
			else:
				for pos_chr in dico_vcf[name_chr]:
					res+=1
				statMEI[chromoMEI]=res
			print("On retrouve", res, "différences sur le chromosome", chromoMEI)
	nombreMEI=[]
	for chromoMEI in statMEI:
		nombreMEI.append(statMEI[chromoMEI])
	moyenne=mean(nombreMEI)
	maximum=max(nombreMEI)
	minimum=min(nombreMEI)
	chromoMax=""
	chromoMin=""
	for chromoMEI in statMEI:
		if statMEI[chromoMEI]!=maximum:
			continue
		elif statMEI[chromoMEI]==maximum:
			chromoMax=chromoMEI
		else:
			print("Impossible de trouver le maximum")
	for chromoMEI in statMEI:
		if statMEI[chromoMEI] != minimum:
			continue
		elif statMEI[chromoMEI]==minimum:
			chromoMin=chromoMEI
		else:
			print("Impossible de trouver le minimum")
	print ("La moyenne est de : ", moyenne,". On retrouve le plus de MEI sur le chromosome ", chromoMax," (avec ",maximum," MEI) et le moins de MEI sur le chromosome ", chromoMin, " (avec ",minimum," MEI).")


def choix(fichier) :
	if fichier==[]:
		sys.exit("FERMETURE DU PROGRAMME !")
	else:
		#HEADER
		check=False
		while check==False:
			choixHeader=input("Voulez-vous afficher le header du fichier VCF ? (Oui/Non)")
			if choixHeader=="Oui":
				check=True
				affichageHeader(extractionHeader(fichier))
				affichageDico(extractionDico(fichier))
			elif choixHeader=="Non":
				check=True
				affichageDico(extractionDico(fichier))
			else:
				print("Veuillez choisir entre Oui ou Non !")
				check=False
		#STAT
		check=False
		while check==False:
			choixStat=input("Voulez-vous afficher quelques stats sur les infos du VCF ? (Oui/Non)")
			if choixStat=="Oui":
				check=True
				statDico(extractionDico(fichier))
			elif choixStat=="Non":
				break
			else: 
				print("Mauvaise saisie, veuillez écrire Oui ou Non.")


###########################################################
#                           MAIN                          #
###########################################################
fichier, listeFichier = ouvertureFichierVCF()
choix(listeFichier)
fermetureFichierVCF(fichier)