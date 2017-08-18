#-*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from subventions.helpers import generate_ordering_arguments, generate_ordering_links
from vos.models import Participation, MontantCheque, Encaissement, EleveVos, Remboursement, Utilisation, SubventionBanque
from binets.models import Mandat, TypeBinet
from django.db.models import Q
from .forms import participationForm, chequeForm, remboursementForm, r_modifForm




@login_required
def home(request):
	"""home page for the vos section"""
	try:
		vos_var = Mandat.objects.get(
			id = request.session['id_mandat'])
	except KeyError:
		return redirect('../')
	# on récupère la liste des utilisateurs habilités
	# à accéder à la page
	authorized = vos_var.get_authorized_users()
	if request.user not in authorized['view'] and not(request.user.is_staff):
		return redirect('../')

	#temporaire
	#v =  TypeBinet.objects.filter(nom='VOS')[0]
	#liste_vos = Mandat.objects.filter(id=mandat)
	#vos_var = liste_vos[0]
	promo = vos_var.promotion

	liste_cheques = MontantCheque.objects.filter(
			evenement=vos_var, 
			).order_by('numero')
	
	liste_participants = Participation.objects.filter(
			evenement=vos_var, 
			participation=True
			).order_by('-eleve__promotion','eleve__nom','eleve__prenom').values('eleve').distinct()
	liste_eleves=[]
	for e in liste_participants:
		liste_eleves.append(EleveVos.objects.filter(id=e['eleve'])[0])

	liste_encaissements=[]
	total_general=0
	total_general1=0
	for e in liste_eleves:
		cheques_perso=[]
		total=0
		total1=0
		for c in liste_cheques:
			p = Encaissement.objects.filter(evenement=vos_var,eleve=e,montant=c)
			if ((len(p)>0) and ((p[0]).paye)):
				total+=c.montant
				total1+=c.montant
				cheques_perso.append(c.montant)
			else:
				cheques_perso.append('')
		r = Remboursement.objects.filter(evenement=vos_var,eleve=e)
		if (len(r)>0):
			remboursement = (r[0]).montant
			total1-=remboursement
		else:
			remboursement = "+"
		lien = "/vos/remboursement/"+str(e.id)
		liste_encaissements.append([e.promotion,e.nom,e.prenom,total,total1,cheques_perso,remboursement,lien])
		total_general+=total
		total_general1+=total1

	return render(request, "vos/home.html", locals())

@login_required
def cheque(request, cheque_numero):
	"""modify a cheque"""

	try:
		vos_var = Mandat.objects.get(
			id = request.session['id_mandat'])
	except KeyError:
		return redirect('../')
	# on récupère la liste des utilisateurs habilités
	# à accéder à la page
	authorized = vos_var.get_authorized_users()
	if request.user not in authorized['view'] and not(request.user.is_staff):
		return redirect('../')
	#on recupere le cheque en question
	try:
		cheque = MontantCheque.objects.get(
			evenement = vos_var,
			numero = cheque_numero)
	except KeyError:
		return redirect('../')
	promo = vos_var.promotion

	if request.POST:
		action = request.POST.get('submit','')
		if action == 'Enregistrer':
			montant=request.POST.get('montant','')
			cheque.montant=montant
			cheque.save()
		if action == 'Ajouter':
			eleve_id = request.POST.get('eleve', '')
			e = EleveVos.objects.filter(id=eleve_id)[0]
			r = Encaissement.objects.filter(
			eleve=e,
			evenement=vos_var,
			montant=cheque)
			if len(r) > 0:
				for p in r:
					p.paye=True
					p.save()
			else:
				p = Encaissement(eleve=e, evenement=vos_var, paye=True, montant=cheque)
				p.save()
		if action == 'Retirer':
			eleve_id = request.POST.get('eleve', '')
			e = EleveVos.objects.filter(id=eleve_id)[0]
			r = Encaissement.objects.filter(
			eleve=e,
			evenement=vos_var,
			montant=cheque)
			if len(r) > 0:
				for p in r:
					p.paye=False
					p.save()
	
	liste_participants = Participation.objects.filter(
			evenement=vos_var, 
			participation=True
			).order_by('-eleve__promotion','eleve__nom','eleve__prenom').values('eleve').distinct()
	liste_eleves=[]
	for e in liste_participants:
		liste_eleves.append(EleveVos.objects.filter(id=e['eleve'])[0])


	form_montant = chequeForm(instance=cheque)


	paye=[]
	for p in liste_eleves:
		requete = Encaissement.objects.filter(
			eleve=p,
			evenement=vos_var,
			montant=cheque)
		paye.append([(len(requete)>0) and ((requete[0]).paye),p.promotion,p.section,p.nom,p.prenom,p.id])
			

	form_paye = participationForm(request.POST or None)

	return render(request, "vos/cheque.html", locals())

@login_required
def nouveau_cheque(request):
	"""create a cheque"""

	try:
		vos_var = Mandat.objects.get(
			id = request.session['id_mandat'])
	except KeyError:
		return redirect('../')
	# on récupère la liste des utilisateurs habilités
	# à accéder à la page
	authorized = vos_var.get_authorized_users()
	if request.user not in authorized['view'] and not(request.user.is_staff):
		return redirect('../')



	numeros = MontantCheque.objects.values_list('numero', flat=True).filter(evenement=vos_var).order_by('-numero')
	if len(numeros)>0:	
		grand = numeros[0]
	else:
		grand=0

	c = MontantCheque(evenement=vos_var, numero=grand+1, montant=0)
	c.save()

	#return redirect('/vos/cheque/'+str(grand+1))
	return redirect('/vos')	

@login_required
def participants(request):
	"""choose who comes to your vos !"""

	try:
		vos_var = Mandat.objects.get(
			id = request.session['id_mandat'])
	except KeyError:
		return redirect('../')
	# on récupère la liste des utilisateurs habilités
	# à accéder à la page
	authorized = vos_var.get_authorized_users()
	if request.user not in authorized['view'] and not(request.user.is_staff):
		return redirect('../')

	promo = vos_var.promotion

	if request.POST:
		eleve_id = request.POST.get('eleve', '')
		e = EleveVos.objects.filter(id=eleve_id)[0]
		action = request.POST.get('submit', '')
		if action == 'Ajouter':
			r = Participation.objects.filter(
			eleve=e,
			evenement=vos_var)
			if len(r) > 0:
				for p in r:
					p.participation=True
					p.save()
			else:
				p = Participation(eleve=e, evenement=vos_var, participation=True)
				p.save()
		if action == 'Retirer':
			r = Participation.objects.filter(
			eleve=e,
			evenement=vos_var)
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
			evenement=vos_var)
		participe.append([(len(requete)>0) and ((requete[0]).participation),p.promotion,p.section,p.nom,p.prenom,p.id])
			

	form = participationForm(request.POST or None)
	
	

	return render(request, "vos/participants.html", locals())


@login_required
def remboursement_modif(request, e_id):
	try:
		vos_var = Mandat.objects.get(
			id = request.session['id_mandat'])
	except KeyError:
		return redirect('../')
	# on récupère la liste des utilisateurs habilités
	# à accéder à la page
	authorized = vos_var.get_authorized_users()
	if request.user not in authorized['view'] and not(request.user.is_staff):
		return redirect('../')

	#on recupere le remboursement en question
	try:
		e = EleveVos.objects.get(id=e_id)
		rs = Remboursement.objects.filter(evenement=vos_var,eleve=e)
	except KeyError:
		return redirect('../')

	if request.POST:
		if rs:
			for r in rs:
				r.montant=request.POST.get('montant','')
				r.eleve=e
				r.save()
		else:
			r = Remboursement(evenement=vos_var,
					montant=request.POST.get('montant',''),
					eleve=e,
					paye=True)
			r.save()
		return redirect('/vos')
	
	if rs:
		modif="Modifier le remboursement de "
		form = r_modifForm(instance=rs[0])
	else:
		modif="Ajouter un remboursement à "
		form = r_modifForm(request.POST or None)

	return render(request, "vos/remboursement.html", locals())


@login_required
def subvention(request, subv):
	"""déterminer qui utilise la subvention subv"""

	try:
		vos_var = Mandat.objects.get(
			id = request.session['id_mandat'])
	except KeyError:
		return redirect('../')
	# on récupère la liste des utilisateurs habilités
	# à accéder à la page
	authorized = vos_var.get_authorized_users()
	if request.user not in authorized['view'] and not(request.user.is_staff):
		return redirect('../')
	promo = vos_var.promotion

	if request.POST:
		action = request.POST.get('submit','')
		if action == 'Enregistrer':
			montant=request.POST.get('montant','')
			cheque.montant=montant
			cheque.save()
		if action == 'Ajouter':
			eleve_id = request.POST.get('eleve', '')
			e = EleveVos.objects.get(id=eleve_id)
			if subv=='banque':
				r = Utilisation.objects.filter(
				eleve=e,
				banque=True)
			if subv=='3A':
				r = Utilisation.objects.filter(
				eleve=e,
				s3a=True)
			if len(r) == 0:
				if subv=='banque':
					p = Utilisation(eleve=e, evenement=vos_var, banque=True)
				if subv=='3A':
					p = Utilisation(eleve=e, evenement=vos_var, s3a=True)
				p.save()
		if action == 'Retirer':
			eleve_id = request.POST.get('eleve', '')
			e = EleveVos.objects.filter(id=eleve_id)[0]
			if subv=='banque':
				r = Utilisation.objects.filter(
				eleve=e,
				banque=True)
			if subv=='3A':
				r = Utilisation.objects.filter(
				eleve=e,
				s3a=True)
			if len(r) > 0:
				for p in r:
					p.delete()
	
	liste_participants = Participation.objects.filter(
			evenement=vos_var, 
			participation=True
			).order_by('-eleve__promotion','eleve__nom','eleve__prenom').values('eleve').distinct()
	paye=[]
	for e in liste_participants:
		p=EleveVos.objects.get(id=e['eleve'])
		if subv=='banque':
			r = Utilisation.objects.filter(
			eleve=p,
			banque=True)
			compte = SubventionBanque.objects.filter(eleve=p)
			condition = (len(compte) > 0) and (compte[0].compte and compte[0].solde and compte[0].actif)
		if subv=='3A':
			r = Utilisation.objects.filter(
			eleve=p,
			s3a=True)
			condition = (p.promotion==promo)
		if condition:
			if len(r)==0:
				paye.append([False,p.promotion,p.section,p.nom,p.prenom,p.id])	
			else:
				if r[0].evenement==vos_var:
					paye.append([True,p.promotion,p.section,p.nom,p.prenom,p.id])
			

	form_paye = participationForm(request.POST or None)

	return render(request, "vos/cheque.html", locals())

@login_required
def subventionB(request):
	return subvention(request, 'banque')
@login_required
def subventionA(request):
	return subvention(request, '3A')
