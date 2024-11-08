import os
from django.core.management.base import BaseCommand
from django.apps import apps
from django.conf import settings


class Command(BaseCommand):
    help = 'Generates views.py and serializers.py based on the models in specified apps.'

    def add_arguments(self, parser):
        # Optional argument to specify apps
        parser.add_argument(
            '--apps',
            nargs='*',
            type=str,
            help='Specify app names to generate views and serializers for, or leave blank to include all user-defined apps.'
        )

    def handle(self, *args, **kwargs):
        # Get user-defined apps from settings or use provided app names
        user_apps = kwargs['apps'] or self.get_user_defined_apps()
        
        for app_name in user_apps:
            try:
                # Get app config and paths
                app_config = apps.get_app_config(app_name)
                views_path = os.path.join(app_config.path, 'views.py')
                serializers_path = os.path.join(app_config.path, 'serializers.py')
                
                # File headers
                views_content = 'from rest_framework import viewsets\n'
                serializers_content = 'from rest_framework import serializers\n'
                views_content += f'from .models import *\n'
                serializers_content += f'from .models import *\n'

                # Loop through models in app
                for model in app_config.get_models():
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

                # Write to serializers.py
                with open(serializers_path, 'w') as serializers_file:
                    serializers_file.write(serializers_content)
                
                # Write to views.py
                with open(views_path, 'w') as views_file:
                    views_file.write(views_content)

                self.stdout.write(self.style.SUCCESS(f'Successfully generated views.py and serializers.py for {app_name}'))

            except LookupError:
                self.stdout.write(self.style.ERROR(f'App {app_name} not found'))

    def get_user_defined_apps(self):
        django_apps = 'django.'
        base_dir = str(settings.BASE_DIR)  # Convert BASE_DIR to a string
        user_apps = [
            app_name for app_name in settings.INSTALLED_APPS 
            if not app_name.startswith(django_apps) and 
               apps.get_app_config(app_name).path.startswith(base_dir)
        ]
        return user_apps
