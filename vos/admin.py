from django.contrib import admin
from .models import MontantCheque, Section, EleveVos, MontantSubventions

class SectionAdmin(admin.ModelAdmin):
	ordering = ('-nom', )

#class Participation(models.Model):
#	"""table de participation a un evenement"""
#	eleve = models.ForeignKey('accounts.Eleve')
#	evenement = models.ForeignKey('vos.Evenement')
#	participation = models.BooleanField()
#
#	def __str__(self):
#		if self.participation:
#			return "{1} participe au {2}".format(self.eleve, self.evenement)
#		else:
#			return "{1} ne participe pas au {2}".format(self.eleve, self.evenement)

class MontantChequeAdmin(admin.ModelAdmin):
	list_display = ('evenement','numero','montant',)
	list_filter = ('evenement', 'numero',)
	ordering = ('evenement', 'numero',)
	search_fields = ('evenement','numero','montant',)

class EleveVosAdmin(admin.ModelAdmin):
	list_display = ('nom','prenom','section')
	list_filter = ('nom','prenom','section')
	ordering = ('section','nom','prenom',)
	search_fields = ('nom','prenom','section')

class MontantSubventionsAdmin(admin.ModelAdmin):
	list_display = ('promotion','banque','vos','jsp','dez')
	list_filter = ('promotion',)
	ordering = ('promotion',)
	search_fields = ('promotion',)
	

admin.site.register(EleveVos, EleveVosAdmin)
admin.site.register(MontantCheque, MontantChequeAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(MontantSubventions, MontantSubventionsAdmin)

#class Encaissement(models.Model):
#	"""table des encaissements par élève"""
#	evenement = models.ForeignKey('vos.Evenement')
#	montant = models.ForeignKey('vos.MontantCheque')
#	eleve = models.ForeignKey('accounts.Eleve')
#	paye = models.BooleanField()
#
#	def __str__(self):
#		return self.montant

#class Remboursement(models.Model):
#	"""table des remboursements par élève"""
#	evenement = models.ForeignKey('vos.Evenement')
#	montant = models.DecimalField(max_digits=5, decimal_places=2)
#	eleve = models.ForeignKey('accounts.Eleve')
#	paye = models.BooleanField()
#
#	def __str__(self):
#		return self.montant
