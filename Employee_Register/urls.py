from django.urls import path
from . import views 

urlpatterns = [

    path('', views.HOME, name='home'),
    path('FirstPage/', views.FirstPage, name='FirstPage'),
    path('FirstPage/statistiques/', views.statistiques_view, name='statistiques'),
    path('FirstPage/insert_auteur', views.auteur_form, name='auteur_insert'),
    path('FirstPage/edit/<int:id>/',views.auteur_form, name='auteur_update'),
    path('FirstPage/auteur_list',views.auteur_list, name='auteur_list'),   
    path('FirstPage/delete/<int:id>/',views.auteur_delete, name='auteur_delete'),

    path('FirstPage/livre/', views.livre_form, name='livre_insert'),
    path('FirstPage/edit_livre/<int:id>/',views.livre_form, name='livre_update'),
    path('FirstPage/delete_livre/<int:id>/', views.livre_delete, name='livre_delete'),  # Ajout de la barre oblique après 'delete'
    path('FirstPage/livre_list',views.livre_list, name='livre_list'),


    path('FirstPage/adherent/', views.adherent_form, name='adherent_insert'),
    path('FirstPage/edit_adherent/<int:id>/',views.adherent_form, name='adherent_update'),
    path('FirstPage/delete_adherent/<int:id>/', views.adherent_delete, name='adherent_delete'),  # Ajout de la barre oblique après 'delete'
    path('FirstPage/adherent_list',views.adherent_list, name='adherent_list'),


    path('emprunt/', views.Emprunt_form, name='emprunt_insert'),
    path('FirstPage/edit_emprunt/<int:id>/',views.Emprunt_form, name='emprunt_update'),
    path('FirstPage/delete_emprunt/<int:id>/', views.Emprunt_delete, name='emprunt_delete'), 
    path('emprunt_list',views.Emprunt_list, name='emprunt_list'),
    path('FirstPage/liste_emprunteurs_livre/<int:livre_id>/', views.liste_emprunteurs_livre, name='liste_emprunteurs_livre'),
]