This package helps in generate the views.py and serializers.py with the auto-generated code.

to generate the serializers and views we need to install our package using:
pip install Django_generate_serializers_views

after installing add the package to the settings.INSTALLED_APPS as :

INSTALLED_APPS = [
    ...,
    'Django_generate_serializers_views',
]

this will help the manage.py to generate the views and serializers with the help of package commands 

use the below command in your django project directorry after defining the model in models.py of your django app.

python manage.py generate_serializers_views