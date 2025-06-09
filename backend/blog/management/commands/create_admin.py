from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import UserProfile
from django.db import transaction


class Command(BaseCommand):
    help = 'Créer un compte administrateur avec le bon rôle'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Nom d\'utilisateur de l\'admin')
        parser.add_argument('--email', type=str, help='Email de l\'admin')
        parser.add_argument('--password', type=str, help='Mot de passe de l\'admin')
        parser.add_argument('--interactive', action='store_true', help='Mode interactif')

    def handle(self, *args, **options):
        if options['interactive'] or not all([options['username'], options['email'], options['password']]):
            self.stdout.write(self.style.SUCCESS('=== Création d\'un compte administrateur ==='))
            
            username = input('Nom d\'utilisateur: ')
            email = input('Email: ')
            password = input('Mot de passe: ')
            first_name = input('Prénom (optionnel): ')
            last_name = input('Nom (optionnel): ')
        else:
            username = options['username']
            email = options['email']
            password = options['password']
            first_name = ''
            last_name = ''

        try:
            with transaction.atomic():
                # Vérifier si l'utilisateur existe déjà
                if User.objects.filter(username=username).exists():
                    self.stdout.write(
                        self.style.ERROR(f'Un utilisateur avec le nom "{username}" existe déjà.')
                    )
                    return

                if User.objects.filter(email=email).exists():
                    self.stdout.write(
                        self.style.ERROR(f'Un utilisateur avec l\'email "{email}" existe déjà.')
                    )
                    return

                # Créer l'utilisateur
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    is_staff=True,
                    is_superuser=True
                )

                # Créer ou mettre à jour le profil avec le rôle admin
                profile, created = UserProfile.objects.get_or_create(user=user)
                profile.role = 'admin'
                profile.bio = 'Administrateur du blog'
                profile.save()

                self.stdout.write(
                    self.style.SUCCESS(
                        f'✅ Compte administrateur créé avec succès !\n'
                        f'   Nom d\'utilisateur: {username}\n'
                        f'   Email: {email}\n'
                        f'   Rôle: {profile.get_role_display()}\n'
                        f'   Superutilisateur Django: Oui\n'
                        f'   Accès admin panel: http://localhost:8000/admin-panel/\n'
                        f'   Accès Django admin: http://localhost:8000/admin/'
                    )
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erreur lors de la création: {str(e)}')
            )