###########################################################
#                        VCF EXE                          #
###########################################################

# Ce script bash permet de modifier l'en-tête des scripts pythons 
#par ceux par défaut sur les OS Ubuntu ou Mac afin de ne pas être 
#obligé de les modifier manuelle à chaque fois. Sauf bien sûr, 
#si python3 (ou les autres versions) ne se trouvent pas dans 
#les répertoires par défaut.

check=false
check2=false
echo "Saississez le répertoire du fichier .cgi ou .py à ouvrir !"
echo "/!\\ Vérifiez bien la saisi, aucun retour en cas d'erreur !"
read fichier

while [ $check = false ]
# Toutes les boucles while permettent de vérifier que la sasie soit correcte
do
	echo "Voulez vous un affichage sur navigateur ou sur console ?"
	echo "(Tapez 'n' pour navigateur et 'c' pour console)"
	read choixAff
	if [ $choixAff = "n" ]
		then
		check=true 
		while [ $check2 = false ]
		do 
			echo "Quelle OS utilisez-vous ? (Tapez mac ou ubuntu) "
			read choixOs
			if [ $choixOs = "mac" ]
				then 
				check2=true
				sed -i -e '1s/.*/#!\/usr\/local\/bin\/python3/' $fichier
				
				# SED est une commande qui permet de modifier le contenu 
				#d'un fichier ici : 
				# - 1s : première ligne
				# - .* : tout ce qu'elle contient
				# - #!... : ce que l'on veut insérer dans le fichier
				# On oublie pas de préciser ensuite où se trouve le fichier à modifier

				/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome http://localhost:8888/cgi-bin/VCF/analyseVCF.cgi
			# On appelle ici le navigateur web suivi de l'adresse de notre cgi 
			# Il n'y a pas d'allias par défaut sur l'ordinateur mac

			elif [ $choixOs = "ubuntu" ]
				then 
				check2=true
				sed -i -e '1s/.*/#!\/usr\/bin\/env python3/' $fichier
				
				chromium-browser http://localhost/~anicolas02/cgi-bin/analyseVCF.cgi
				# Pour Ubuntu, en ce qui concerne les ordinateurs de la fac, l'allias
				#firefox réfère le répertoire où se trouve le navigateur, on ajoute juste 
				#à la commande le lien.  

			else
				echo "Le choix que vous demandez n'existe pas..."
				echo "Fermeture du programme."
			fi
		done
	elif [ $choixAff = "c" ]
		then 
		check=true
		while [ $check2 = false ]
		do 
			echo "Quelle OS utilisez-vous ? (Tapez mac ou ubuntu) "
			read choixOs
			if [ $choixOs = "mac" ]
				then 
				check2=true
				sed -i -e '1s/.*/#!\/usr\/local\/bin\/python3/' $fichier
				chmod 755 test.py
				./$fichier
			elif [ $choixOs = "ubuntu" ]
				then 
				check2=true
				sed -i -e '1s/.*/#!\/usr\/bin\/env python3/' $fichier
				chmod 755 test.py
				./$fichier
			else
				echo "Le choix que vous demandez n'existe pas..."
				echo "Fermeture du programme."
			fi
		done
	else
		echo "Le choix que vous demandez n'existe pas..."
		echo "Fermeture du programme."
	fi
done
