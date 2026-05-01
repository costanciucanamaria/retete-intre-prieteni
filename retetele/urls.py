from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_retete, name='retete'),
    path('introducere_reteta/', views.introducere_reteta, name='introducere_reteta'),
    path('reteta/<int:pk>/stergere_reteta/', views.stergere_reteta, name='stergere_reteta'),
    path('reteta/<int:pk>/modificare_reteta/', views.modificare_reteta, name='modificare_reteta'),
    path('reteta/<int:pk>/adauga_poza/', views.adauga_poza, name="adauga_poza"),
    path('reteta/<int:pk>/sterge_poza/', views.sterge_poza, name="sterge_poza"),
    path('prieteni/<int:pk>/retete/', views.retetele_prietenilor, name="retetele_prietenilor"),
    path('cautare', views.cautare_retete, name="cautare_retete"),
    path('reteta/<int:pk>/comment/', views.adauga_comment, name='adauga_comment'),
    path('reteta/<int:pk>/like/', views.adauga_like, name='adauga_like'),
]

if settings.DEBUG:
   urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)