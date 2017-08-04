#-*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from subventions.helpers import generate_ordering_arguments, generate_ordering_links
from vos.models import Participation, MontantCheque, Encaissement, EleveVos
from binets.models import Mandat, TypeBinet
from django.db.models import Q
from .forms import participationForm




@login_required
def home(request):
	"""home page for the vos section"""

	#temporaire
	v =  TypeBinet.objects.filter(nom='VOS')[0]
	liste_vos = Mandat.objects.filter(Q(type_binet=v))
	vos_var = liste_vos[0]
	promo = vos_var.promotion

	liste_cheques = MontantCheque.objects.filter(
			evenement=vos_var, 
			promotion=promo
			).order_by('ordre')
	
	liste_participants = Participation.objects.filter(
			evenement=vos_var, 
			promotion=promo
			).order_by('eleve')

	return render(request, "vos/home.html", locals())

@login_required
def participants(request):
	"""home page for the vos section"""

	

	#temporaire
	v =  TypeBinet.objects.filter(nom='VOS')[0]
	liste_vos = Mandat.objects.filter(Q(type_binet=v))
	vos_var = liste_vos[0]
	promo = vos_var.promotion

	if request.POST:
		eleve_id = request.POST.get('eleve', '')
		e = EleveVos.objects.filter(id=eleve_id)[0]
		action = request.POST.get('submit', '')
		if action == 'Ajouter':
			r = Participation.objects.filter(
			eleve=e,
			evenement=vos_var,
			promotion=promo)
			if len(r) > 0:
				for p in r:
					p.participation=True
					p.save()
			else:
				p = Participation(eleve=e, evenement=vos_var, promotion=promo, participation=True)
				p.save()
		if action == 'Retirer':
			r = Participation.objects.filter(
			eleve=e,
			evenement=vos_var,
			promotion=promo)
			if len(r) > 0:
				for p in r:
					p.participation=False
					p.save()

	# paramètre d'ordonnance
	ordering = request.GET.get('o', None)
	
	attributes = ['section', 'promotion', 'nom', 'prenom']

	# on génère les arguments d'ordonnance de la liste
	arguments = generate_ordering_arguments(ordering, attributes)

	
	# on génère les liens qui serviront à l'ordonnance dans la page
	# si aucun n'a été activé, par défault c'est par nom de binet (index 0)
	# sachant qu'on va accéder aux éléments par pop(), on doit inverser l'ordre
	links_base = '?o='
	ordering_links = list(reversed(generate_ordering_links(ordering, attributes, links_base)))
	
	if arguments:
		liste_section = EleveVos.objects.filter().order_by(*arguments)
	else:
		liste_section = EleveVos.objects.filter().order_by('section','promotion','nom','prenom')

	participe=[]
	for p in liste_section:
		requete = Participation.objects.filter(
			eleve=p,
			evenement=vos_var,
			promotion=promo)
		participe.append([(len(requete)>0) and ((requete[0]).participation),p.promotion,p.section,p.nom,p.prenom,p.id])
			

	form = participationForm(request.POST or None)
	
	

	return render(request, "vos/participants.html", locals())

