# Generated by Django 5.0.3 on 2024-04-09 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Employee_Register', '0004_adherent_emprunt'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emprunt',
            name='date_retour_effective',
        ),
        migrations.AlterField(
            model_name='emprunt',
            name='date_retour_prevue',
            field=models.DateField(blank=True, null=True),
        ),
    ]
