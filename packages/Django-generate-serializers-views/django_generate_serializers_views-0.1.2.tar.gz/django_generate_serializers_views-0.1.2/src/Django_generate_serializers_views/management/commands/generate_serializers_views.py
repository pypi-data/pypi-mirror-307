import os
from django.core.management.base import BaseCommand
from django.apps import apps
from django.conf import settings


class Command(BaseCommand):
    help = 'Generates views.py and serializers.py based on the models in specified apps.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--apps',
            nargs='*',
            type=str,
            help='Specify app names to generate views and serializers for, or leave blank to include all user-defined apps.'
        )

    def handle(self, *args, **kwargs):
        user_apps = kwargs['apps'] or self.get_user_defined_apps()
        print(f"User-defined apps: {user_apps}")
        
        for app_name in user_apps:
            try:
                app_config = apps.get_app_config(app_name)
                views_path = os.path.join(app_config.path, 'views.py')
                serializers_path = os.path.join(app_config.path, 'serializers.py')

                views_content = 'from rest_framework import viewsets\n'
                serializers_content = 'from rest_framework import serializers\n'
                views_content += f'from .models import *\n'
                views_content += f'from .serializers import *\n'
                serializers_content += f'from .models import *\n'

                # Check if models exist in the app
                models_found = False  # Flag to track if any models are found

                for model in app_config.get_models():
                    models_found = True
                    model_name = model.__name__
                    serializers_content += f"""
class {model_name}Serializer(serializers.ModelSerializer):
    class Meta:
        model = {model_name}
        fields = '__all__'
"""
                    views_content += f"""
class {model_name}ViewSet(viewsets.ModelViewSet):
    queryset = {model_name}.objects.all()
    serializer_class = {model_name}Serializer
"""

                # Notify if no models are found in the app
                if not models_found:
                    self.stdout.write(self.style.WARNING(f'No models found in app "{app_name}".'))
                    continue

                with open(serializers_path, 'w') as serializers_file:
                    serializers_file.write(serializers_content)
                
                with open(views_path, 'w') as views_file:
                    views_file.write(views_content)

                self.stdout.write(self.style.SUCCESS(f'Successfully generated views.py and serializers.py for "{app_name}".'))

            except LookupError:
                self.stdout.write(self.style.ERROR(f'App "{app_name}" not found'))

    def get_user_defined_apps(self):
        excluded_package = 'Django_generate_serializers_views'
        django_apps = 'django.'
        user_apps = [
            app_name for app_name in settings.INSTALLED_APPS 
            if not app_name.startswith(django_apps) and 
               apps.get_app_config(app_name).path.startswith(str(settings.BASE_DIR)) and
               app_name != excluded_package
        ]
        return user_apps
