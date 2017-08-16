from django.forms import ModelForm
from .models import Participation, MontantCheque, Remboursement
from django.utils.translation import ugettext_lazy as _

class participationForm(ModelForm):
	class Meta:
		model = Participation
		fields = []
		labels = {}

class chequeForm(ModelForm):
	class Meta:
		model = MontantCheque
		fields = ['montant']
		#labels = {}

class remboursementForm(ModelForm):
	class Meta:
		model = Remboursement
		fields = ['eleve','montant']
		labels = {}

class r_modifForm(ModelForm):
	class Meta:
		model = Remboursement
		fields = ['montant']
		#labels = {}
