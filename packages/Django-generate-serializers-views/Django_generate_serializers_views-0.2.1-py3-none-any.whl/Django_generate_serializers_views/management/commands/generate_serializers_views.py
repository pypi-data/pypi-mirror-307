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

                # Define import statements
                views_imports = [
                    'from rest_framework import viewsets\n',
                    'from .models import *\n',
                    'from .serializers import *\n'
                ]
                serializers_imports = [
                    'from rest_framework import serializers\n',
                    'from .models import *\n'
                ]

                # Load existing file contents
                existing_views_content = self.read_file_content(views_path)
                existing_serializers_content = self.read_file_content(serializers_path)

                # Filter out missing imports to add only those not present in existing content
                views_imports_to_add = [imp for imp in views_imports if imp not in existing_views_content]
                serializers_imports_to_add = [imp for imp in serializers_imports if imp not in existing_serializers_content]

                # Initialize content for new classes
                new_views_content = ""
                new_serializers_content = ""

                models_found = False
                
                for model in app_config.get_models():
                    model_name = model.__name__
                    models_found = True

                    # Serializer class definition
                    serializer_class_def = f'class {model_name}Serializer(serializers.ModelSerializer):'
                    if serializer_class_def not in existing_serializers_content:
                        new_serializers_content += f"""
class {model_name}Serializer(serializers.ModelSerializer):
    class Meta:
        model = {model_name}
        fields = '__all__'
"""

                    # Viewset class definition
                    viewset_class_def = f'class {model_name}ViewSet(viewsets.ModelViewSet):'
                    if viewset_class_def not in existing_views_content:
                        new_views_content += f"""
class {model_name}ViewSet(viewsets.ModelViewSet):
    queryset = {model_name}.objects.all()
    serializer_class = {model_name}Serializer
"""

                if not models_found:
                    self.stdout.write(self.style.WARNING(f'No models found in app "{app_name}".'))
                    continue

                # Write serializers.py: add imports at the top, then append new classes if any
                if serializers_imports_to_add or new_serializers_content.strip():
                    with open(serializers_path, 'w') as serializers_file:
                        serializers_file.write("".join(serializers_imports_to_add) + "\n" + existing_serializers_content + new_serializers_content)

                # Write views.py: add imports at the top, then append new classes if any
                if views_imports_to_add or new_views_content.strip():
                    with open(views_path, 'w') as views_file:
                        views_file.write("".join(views_imports_to_add) + "\n" + existing_views_content + new_views_content)

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

    def read_file_content(self, file_path):
        """Reads the content of a file if it exists, otherwise returns an empty string."""
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                return file.read()
        return ""
