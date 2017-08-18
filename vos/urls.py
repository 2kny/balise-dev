from django.conf.urls import url

from . import views


urlpatterns = [

	url(r'^$', views.home),
	url(r'^liste$', views.participants),
	url(r'^cheque/(?P<cheque_numero>\d+)$', views.cheque, name='cheque_numero'),
	url(r'^cheque$', views.nouveau_cheque),
	url(r'^remboursement/(?P<e_id>\d+)$', views.remboursement_modif, name='e_id'),
	url(r'^subvention/banque$', views.subventionB),
	url(r'^subvention/3A$', views.subventionA),

    
]
