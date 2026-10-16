cd YapeRegistro
python3.14 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
DJANGO_DEMO_MODE=true python manage.py runserver