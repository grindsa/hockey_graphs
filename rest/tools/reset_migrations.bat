python3 manage.py migrate --fake rest zero
del rest\migrations\00*.py
python3 manage.py makemigrations
python3 manage.py migrate --fake-initial