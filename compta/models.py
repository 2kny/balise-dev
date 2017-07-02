from django.db import models






################################################
class TypeBinet(models.Model):
	"""types de binets
	ces types peuvent être
	avec chéquier, sans chéquier, ou compte exté"""
	nom = models.CharField(max_length=30)

	def __str__(self):
		return self.nom


class Mandat(models.Model):
	"""correspondance entre le binet et ses membres"""
	binet = models.ForeignKey('Binet')
	president = models.ForeignKey('accounts.Eleve', related_name = "president")
	tresorier = models.ForeignKey('accounts.Eleve', related_name = "tresorier")

	def __str__(self):
		return str(self.id)





class Binet(models.Model):
	"""table dans la BDD représentant l'ensemble des binets"""
	nom = models.CharField(max_length=100)
	description = models.TextField(blank=True, null = True) # facultatif
	type_binet = models.ForeignKey('TypeBinet', verbose_name = "chéquier")
	remarques_admins = models.TextField(blank=True, null = True) # facultatif
	is_active = models.BooleanField(verbose_name = "Actif")
	current_president = models.ForeignKey('accounts.Eleve', verbose_name = "Président", related_name = "current_president")
	current_tresorier = models.ForeignKey('accounts.Eleve', verbose_name = "Trésorier", related_name = "current_tresorier")
	current_promotion = models.ForeignKey('accounts.Promotion', verbose_name = "Promo")

	def __str__(self):
		return self.nom


class LigneCompta(models.Model):
	"""opérations comptables"""
	binet = models.ForeignKey('Binet')
	date = models.DateField(auto_now_add=False, auto_now=False, 

                                verbose_name="Effectuée le")
	auteur = models.ForeignKey('accounts.Eleve', verbose_name = 'Par')
	description = models.CharField(max_length=200)
	debit = models.FloatField(blank = True, null = True)
	credit = models.FloatField(blank = True, null = True)

	def __str__(self):
		return self.description