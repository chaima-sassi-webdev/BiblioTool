from django.db import models
from django.utils import timezone
from datetime import timedelta

# Create your models here.
class Auteur(models.Model): 
	code_auteur = models.IntegerField()
	Nom_auteur = models.CharField(max_length=50)
	Prenom_auteur = models.CharField(max_length=50)


	def __str__(self):
		return f"{self.Nom_auteur} {self.Prenom_auteur}"



class Livre(models.Model):
    code_livre = models.IntegerField()
    Titre_livre = models.CharField(max_length=50)
    Nbre_page = models.IntegerField()
    disponible = models.BooleanField(default=True)
    exemplaires = models.IntegerField(default=1)  
    Nom_auteur = models.ForeignKey(Auteur, on_delete=models.CASCADE)


    def __str__(self):
        etat = "Disponible" if self.disponible else "Emprunté"
        return f"{self.Titre_livre} - {self.Nom_auteur} ({etat})"



class Adherent(models.Model):
    code_adh = models.IntegerField()
    nom_adh = models.CharField(max_length=50)
    nbrEmprunts_adh = models.IntegerField(default=0)

    def __str__(self):
        return self.nom_adh


class Emprunt(models.Model):

    livre = models.ForeignKey(Livre, on_delete=models.CASCADE)
    adherent = models.ForeignKey(Adherent, on_delete=models.CASCADE)
    date_emprunt = models.DateField(default=timezone.now)
    date_retour_prevue = models.DateField(null=True, blank=True)
    date_retour = models.DateField(null=True, blank=True)
    retard= models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.date_retour_prevue:
            self.date_retour_prevue = self.date_emprunt + timedelta(days=15)
        super().save(*args, **kwargs)

    def est_en_retard(self):
        return self.date_retour_prevue and self.date_retour_prevue < timezone.now()

    def __str__(self):
        return f"Emprunt de '{self.livre}' par '{self.adherent}'"
