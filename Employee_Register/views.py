import matplotlib
matplotlib.use('Agg')
from django.shortcuts import render, redirect, get_object_or_404
from .forms import AuteurForm ,LivreForm,AdherentForm, EmpruntForm
from .models import Auteur,Livre,Adherent, Emprunt
from django.db.models import F , Subquery, OuterRef
from django.utils import timezone
from datetime import datetime
from django.conf import settings
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from django.http import HttpResponse, HttpRequest
import os
import pandas as pd
import logging
logger = logging.getLogger(__name__)

#Fonction pour créer et modifier un auteur
def HOME(request):
    timestamp = timezone.now()
    return render(request, 'app.html', {'timestamp': timestamp})
def FirstPage(request):
    return render(request, 'first-page.html', {})
    
def auteur_form(request, id=0):
    if request.method == "GET":
        if id == 0: #Création d'un nouvel auteur
            form = AuteurForm()
        else:
            auteur = Auteur.objects.get(pk=id)
            form = AuteurForm(instance=auteur)
        return render(request, 'auteur/auteur_form.html', {'form': form})
    else:
        if id == 0:
            form = AuteurForm(request.POST)
        else:  # Modification d'un auteur
            auteur = Auteur.objects.get(pk=id)
            form = AuteurForm(request.POST, instance=auteur)
        if form.is_valid():
            form.save()
        return redirect('/auteur_list')

#Afficher la liste des auteurs

def auteur_list(request):
    auteur_list = Auteur.objects.all().order_by('Nom_auteur')  # Triez les auteurs par le champ 'Nom_auteur'
    context = {'auteur_list': auteur_list}
    return render(request, 'auteur/auteur_list.html', context)
#Effacer un auteur

def auteur_delete(request, id):
    auteurs = Auteur.objects.get(pk=id)
    auteurs.delete()
    return redirect('/auteur_list')

# Méthode pour la création et la modification d'un nouvel livre

def livre_form(request, id=0):
    if request.method == "GET":
        if id == 0:
            form = LivreForm()
        else:
            livre = Livre.objects.get(pk=id)
            form = LivreForm(instance=livre)
        return render(request, 'livre/livre_form.html', {'form': form})
    else:
        if id == 0:
            form = LivreForm(request.POST)
        else:
            livre = Livre.objects.get(pk=id)
            form = LivreForm(request.POST, instance=livre)
        if form.is_valid():
            form.save()
        return redirect('/livre_list')


# Méthode pour la suppression d'un  livre

def livre_delete(request, id):
    livres = Livre.objects.get(pk=id)
    livres.delete()
    return redirect('/livre_list')

# Méthode pour l'affichage d'une liste

def livre_list(request):
    livre_list = Livre.objects.all().order_by('Titre_livre')  # Triez les auteurs par le champ 'Titre_livre'
    context = {'livre_list': livre_list}
    return render(request, 'livre/livre_list.html', context)



# Fonction pour la création et la modification d'un nouvel adhérent

def adherent_form(request, id=0):
    if request.method == "GET":
        if id == 0:
            form = AdherentForm()
        else:
            adherent = Adherent.objects.get(pk=id)
            form = AdherentForm(instance=adherent)
        return render(request, 'adherent/adherent_form.html', {'form': form})
    else:
        if id == 0:
            form = AdherentForm(request.POST)
        else:
            adherent = Adherent.objects.get(pk=id)
            form = AdherentForm(request.POST, instance=adherent)
        if form.is_valid():
            form.save()
        return redirect('/adherent_list')

# Méthode pour la suppression d'un  adhérent

def adherent_delete(request, id):
    adherent = Adherent.objects.get(pk=id)
    adherent.delete()
    return redirect('/adherent_list')

# Méthode pour l'affichage d'une liste  d'adhérent

def adherent_list(request):
    adherent_list = Adherent.objects.all().order_by('nom_adh')  # Triez les auteurs par le champ 'nom_adh'
    context = {'adherent_list': adherent_list}
    return render(request, 'adherent/adherent_list.html', context)

# Fonction pour la création et la modification d'un nouvel emprunt

def Emprunt_form(request, id=0):
    if request.method == "POST":
        if id == 0:
            form = EmpruntForm(request.POST)
        else:
            emprunt = get_object_or_404(Emprunt, pk=id)
            form = EmpruntForm(request.POST, instance=emprunt)

        if form.is_valid():
            emprunt = form.save(commit=False)
            emprunt.date_retour = form.cleaned_data['date_retour']
            emprunt.date_retour_prevue = form.cleaned_data['date_retour_prevue']
            emprunt.save()
            return redirect('/emprunt_list')
    else:
        if id != 0:
            emprunt = get_object_or_404(Emprunt, pk=id)
            form = EmpruntForm(instance=emprunt)
        else:
            form = EmpruntForm()

    return render(request, 'emprunt/Emprunt_form.html', {'form': form})

# Méthode pour la suppression d'un  emprunt

def Emprunt_delete(request, id):
    emprunts = Emprunt.objects.get(pk=id)
    emprunts.delete()
    return redirect('/emprunt_list')

# Méthode pour l'affichage d'une liste  d'emprunt

def Emprunt_list(request):
    emprunt_list = Emprunt.objects.all()
    context = {'emprunt_list': emprunt_list} 
    return render(request, 'emprunt/emprunt_list.html', context)

def liste_emprunteurs_livre(request, livre_id):
    livre = get_object_or_404(Livre, id=livre_id)
    
    # Récupérer tous les emprunts associés à ce livre avec les adhérents préchargés
    emprunts = Emprunt.objects.filter(livre=livre).select_related('adherent')
    
    # Créer une liste vide pour stocker les adhérents et les emprunts en retard
    adherents = []
    emprunts_retard = []
    livres_non_retournes = []
    
    # Parcourir les emprunts pour obtenir les adhérents et vérifier les retards
    for emprunt in emprunts:
        adherent = emprunt.adherent
        adherents.append(adherent)
        
        if emprunt.date_retour and emprunt.date_retour_prevue:
            # Vérifier si l'emprunt est en retard et le marquer comme tel
            if emprunt.date_retour > emprunt.date_retour_prevue:
                emprunt.retard = True
                emprunts_retard.append(emprunt)
            else:
                emprunt.retard = False
        else:
            # Si l'une des dates de retour est None, marquez l'emprunt comme en retard
            emprunt.retard = True
            emprunts_retard.append(emprunt)

    
    # Passer le livre, la liste des adhérents, les emprunts et les livres non retournés au template
    return render(request, 'emprunt/liste_emprunteurs_livre.html', {'livre': livre, 'adherents': adherents, 'emprunts': emprunts, 'emprunts_retard': emprunts_retard, 'livres_non_retournes': livres_non_retournes})

def histogramme_livres_plus_empruntes(request):
    emprunts = Emprunt.objects.select_related('livre').all()
    # Créer un DataFrame avec l'ID et le titre du livre
    # df_emprunts = pd.DataFrame(list(emprunts.values('livre_id')))
    
    # # Compter les emprunts par titre de livre
    # comptage_livres = df_emprunts['livre_id'].value_counts()
    
    # Sélectionner les 10 livres les plus empruntés
    # top_livres = comptage_livres.head(10)
    # fig, ax = plt.subplots()
    # top_livres.plot(kind='bar', color='skyblue', ax=ax)
    # ax.set_yticks(range(0, top_livres.max() + 1, 1))
    # # Ajouter des étiquettes aux barres

    # plt.xlabel('Livres')
    # plt.ylabel("Nombre d'emprunts")
    # plt.title('Histogramme des livres les plus empruntés')
    # chemin_image = os.path.join(settings.STATICFILES_DIRS[0], 'statistiques/images/histogramme_livres_plus_empruntes.png')
    # plt.savefig(chemin_image)   
    # # Renvoyer le template HTML avec le chemin vers l'image
    return render(request, 'statistiques/statistiques.html', {'chemin_image_livres':'statistiques/images/histogramme_livres_plus_empruntes.png'})

def histogramme_emprunts_par_classe(emprunts):
    # plt.switch_backend('Agg')  # Utiliser un backend non interactif
    # emprunts = Emprunt.objects.values('date_retour_prevue', 'retard')
    # df_emprunts = pd.DataFrame(emprunts)
    # df_emprunts['date_retour_prevue'] = pd.to_datetime(df_emprunts['date_retour_prevue'])
    # print(df_emprunts['date_retour_prevue'])
    # # Sélectionner les livres disponibles
    # livres_disponibles = df_emprunts[df_emprunts['retard'] == False]
    # # Sélectionner les livres non retournés
    # livres_non_retournes = df_emprunts[df_emprunts['retard'] == True]
    # min_date = df_emprunts['date_retour_prevue'].min()
    # max_date= df_emprunts['date_retour_prevue'].max()
    # # Créer une nouvelle figure et les axes
    # fig, ax = plt.subplots()
    # # Définir l'échelle de l'axe x à partir de la première date de retour prévue
    # date_formatter = mdates.DateFormatter('%m/%Y')  # Format mois en nombre et année
    # ax.xaxis.set_major_formatter(date_formatter)
    # # Espacer les étiquettes des mois
    # ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    # # Définir l'échelle de l'axe y par pas de 1
    # ax.set_yticks(range(0, int(max(len(livres_disponibles), len(livres_non_retournes))) + 1, 1))

    # # Tracer l'histogramme des livres disponibles
    # livres_disponibles['date_retour_prevue'].hist(ax=ax, color='lightgreen', bins=10, alpha=0.7, label='Livres disponibles')

    # # Tracer l'histogramme des livres non retournés
    # livres_non_retournes['date_retour_prevue'].hist(ax=ax, color='salmon', bins=10, alpha=0.7, label='Livres non retournés')

    # # Ajouter les labels, titre et légende
    # ax.set_xlabel('Date de retour prévue')
    # plt.legend()
    # ax.xaxis.label.set_size(10)
    # # Enregistrer l'image
    # chemin_image = os.path.join(settings.STATICFILES_DIRS[0], 'statistiques/images/histogramme_emprunts_par_classe.png')
    # plt.savefig(chemin_image)

    # # Retourner le chemin d'accès de l'image enregistrée
    return render(request, 'statistiques/statistiques.html', {})

def statistiques_view(request):
    # emprunts = Emprunt.objects.all()
    # histogramme_livres_plus_empruntes(request)  # Passer l'objet request
    # emprunts_non_retournes = Emprunt.objects.filter(retard=True)
    # histogramme_emprunts_par_classe(emprunts_non_retournes)
    # chemin_image_livres = 'statistiques/images/histogramme_livres_plus_empruntes.png'
    # chemin_image_classe = 'statistiques/images/histogramme_emprunts_par_classe.png'
    return render(request, 'C:/Users/pc/Desktop/projet_python/Gestion_Bibliotheques/Employee_project/Employee_Register/template/statistiques/statistiques.html' ,{})