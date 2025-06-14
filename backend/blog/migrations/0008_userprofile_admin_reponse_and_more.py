# Generated by Django 5.2.1 on 2025-06-04 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_alter_commentaire_options_article_date_modification_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='admin_reponse',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='admin_reponse_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='demande_auteur_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='demande_auteur_message',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='demande_auteur_statut',
            field=models.CharField(choices=[('aucune', 'Aucune demande'), ('en_attente', 'En attente'), ('acceptee', 'Acceptée'), ('refusee', 'Refusée')], default='aucune', max_length=20),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='role',
            field=models.CharField(choices=[('lecteur', 'Lecteur'), ('auteur', 'Auteur'), ('admin', 'Administrateur')], default='lecteur', max_length=20),
        ),
    ]
