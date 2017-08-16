from django.db import models
from binets.models import Binet, Mandat

class Section(models.Model):
	"""table des sections"""
	nom = models.CharField(max_length=20)

	class Meta:
		ordering = ('-nom',)

	def __str__(self):
		return self.nom

class EleveVos(models.Model):
	"""eleves par section et promotion"""
	section = models.ForeignKey('vos.Section')
	promotion = models.ForeignKey('accounts.Promotion')
	nom = models.CharField(max_length=100)
	prenom = models.CharField(max_length=100)
	
	def __str__(self):
		return "{0} {1}".format(self.prenom, self.nom)		
	
	class Meta:
		ordering = ['nom','prenom']

class Participation(models.Model):
	"""table de participation a un evenement"""
	eleve = models.ForeignKey('vos.EleveVos')
	evenement = models.ForeignKey('binets.Mandat')
	participation = models.BooleanField()

	def __str__(self):
		if self.participation:
			return "{0} participe au {1}".format(self.eleve, self.evenement)
		else:
			return "{0} ne participe pas au {1}".format(self.eleve, self.evenement)

class MontantCheque(models.Model):
	"""table des montants des différents chèques"""
	evenement = models.ForeignKey('binets.Mandat')
	numero = models.IntegerField()
	montant = models.DecimalField(max_digits=5, decimal_places=2)	

	def __str__(self):
		return "Chèque n°{0} : {1} €".format(self.numero, self.montant)

	@models.permalink
	def get_cheque_numero(self):
		"""returns the link to the cheque form"""
		return ('cheque_numero', [self.numero])

class Encaissement(models.Model):
	"""table des encaissements par élève"""
	evenement = models.ForeignKey('binets.Mandat')
	montant = models.ForeignKey('vos.MontantCheque')
	eleve = models.ForeignKey('vos.EleveVos')
	paye = models.BooleanField()

	def __str__(self):
		return self.montant

class Remboursement(models.Model):
	"""table des remboursements par élève"""
	evenement = models.ForeignKey('binets.Mandat')
	montant = models.DecimalField(max_digits=5, decimal_places=2)
	eleve = models.ForeignKey('vos.EleveVos')
	paye = models.BooleanField()

	def __str__(self):
		return self.montant

	@models.permalink
	def get_remboursement_numero(self):
		"""returns the link to the remboursement modification form"""
		return ('remboursement_id', [self.id])
