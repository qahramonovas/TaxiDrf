create_app:
	python3 manage.py startapp management

create_user:
	python3 manage.py createsuperuser


mig:
	python3 manage.py makemigrations
	python3 manage.py migrate