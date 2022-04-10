py manage.py migrate --fake rest zero
del rest\migrations\00*.py
py manage.py makemigrations
py manage.py migrate --fake-initial