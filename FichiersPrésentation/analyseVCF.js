'use strict';

//Cette fonction va changer l'icone + ou - quand on clique dessus
function cliqueIconePlusMoins(){
	var icone = document.querySelector('.plus-toggle i'); //on recupere le clique (ou non) sur licone +du header
	//on traite : si cest l'icone + alors on met licone - et inversement
	icone.classList.toggle('fa-plus'); // classList retourne la liste des classes avec 'fa-plus'
    icone.classList.toggle('fa-minus');
}

//Cette fonction va affichier ou cacher les données quand on clique dessus
function cliqueAfficherDonnees(){
	var donnees = document.querySelector(".description div");
	donnees.classList.toggle("hide"); // car hideau debut
}

//quand tu cliques, tu declenches levenement en appelant la fonction
document.querySelector(".plus-toggle i").addEventListener('click', cliqueIconePlusMoins);
document.querySelector('.plus-toggle i').addEventListener('click', cliqueAfficherDonnees);


