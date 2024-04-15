from django.contrib import admin
from .models import Auteur, Adherent , Livre , Emprunt
# Register your models here.


admin.site.register(Auteur)
admin.site.register(Livre)
admin.site.register(Adherent)
admin.site.register(Emprunt)