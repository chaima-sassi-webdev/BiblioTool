from django import  forms
from .models import Auteur,Adherent, Emprunt, Livre

class AuteurForm(forms.ModelForm):
    class Meta:
        model = Auteur
        fields = [
            'code_auteur',
            'Nom_auteur',
            'Prenom_auteur'
        ]
        labels = {
            'code_auteur': 'Code',
            'Nom_auteur': 'Nom',
            'Prenom_auteur': 'Prénom',
        }

    def __init__(self, *args, **kwargs):
        super(AuteurForm, self).__init__(*args, **kwargs)



class LivreForm(forms.ModelForm):
    class Meta:
        model = Livre
        fields = [
            'code_livre',
            'Titre_livre',
            'Nbre_page', 
            'Nom_auteur',
            'exemplaires',
            'disponible',        
        ]
        labels = {
            'code_livre':'Code',
            'Titre_livre':'Titre',
            'Nbre_page': 'Nombre de page',
            'Nom_auteur': 'Nom auteur',
            'exemplaires' : 'Exemplaires',
            'disponible' : 'Disponible',
        }
        widgets = {
            'Nom_auteur': forms.Select(choices=[(auteur.id, f"{auteur.Nom_auteur} {auteur.Prenom_auteur}") for auteur in Auteur.objects.all()])
        }

    def __init__(self, *args, **kwargs):
        super(LivreForm, self).__init__(*args, **kwargs)
        self.fields['Nom_auteur'].queryset = Auteur.objects.all()


class AdherentForm(forms.ModelForm):
    class Meta:
        model = Adherent
        fields = [
            'code_adh',
            'nom_adh',
            'nbrEmprunts_adh',
        ]
        labels = {
            'code_adh': 'Code',
            'nom_adh': 'Nom',
            'nbrEmprunts_adh': 'Nombre d\'emprunts',
        }



class EmpruntForm(forms.ModelForm):
    class Meta:
        model = Emprunt
        fields = [
            'adherent',
            'livre',
            'date_emprunt',
            'date_retour',
            'date_retour_prevue',
            'retard',        
        ]
        labels = {
            'adherent': 'Adhérent',
            'livre': 'Livre',
            'date_emprunt': 'Date d\'emprunt',
            'date_retour': 'Date de retour',
            'date_retour_prevue': 'Date de retour prévue',
            'retard': 'retard',
        }
        widgets = {
            'adherent': forms.Select(choices=[(adherent.id, adherent.nom_adh) for adherent in Adherent.objects.all()]),
            'livre': forms.Select(choices=[(livre.id, livre.Titre_livre) for livre in Livre.objects.filter(disponible=True)]),
            'date_emprunt': forms.DateInput(attrs={'type': 'date'}),
            'date_retour': forms.DateInput(attrs={'type': 'date'}),
            'date_retour_prevue': forms.DateInput(attrs={'type': 'date'}),
            'retard': forms.DateInput(attrs={'type': 'boolean'}),
        }

    def __init__(self, *args, **kwargs):
        super(EmpruntForm, self).__init__(*args, **kwargs)
        self.fields['adherent'].queryset = Adherent.objects.all()
        self.fields['livre'].queryset = Livre.objects.filter(disponible=True)

    def clean(self):
        cleaned_data = super().clean()
        adherent = cleaned_data.get('adherent')
        livre = cleaned_data.get('livre')
        
        # Vérifier si l'adhérent a déjà emprunté le même livre
        if Emprunt.objects.filter(adherent=adherent, livre=livre).exists():
            self.add_error('livre', "Cet adhérent a déjà emprunté ce livre.")
        
        return cleaned_data