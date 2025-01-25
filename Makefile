run:
	python3.11 -m venv venv
	. ./venv/bin/activate && pip install -r requirements.txt
	. ./venv/bin/activate && python config/manage.py migrate
	. ./venv/bin/activate && python config/manage.py runserver 8000

migrate:
	. ./venv/bin/activate && python config/manage.py makemigrations
	. ./venv/bin/activate && python config/manage.py migrate

