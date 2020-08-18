bash:
	docker exec -it djangoplicity-actions-web bash

test:
	docker exec -it djangoplicity-actions-web coverage run --source='.' manage.py test

makemigrations:
	docker exec -it djangoplicity-actions-web python manage.py makemigrations test_project

migrate:
	docker exec -it djangoplicity-actions-web python manage.py migrate test_project

coverage-html:
	docker exec -it djangoplicity-actions-web coverage html
	google-chrome htmlcov/index.html

test-python27:
	docker exec -it djangoplicity-actions-web tox -e py27-django111

test-python37:
	docker exec -it djangoplicity-actions-web tox -e py37-django22	

futurize-stage1:
	docker exec -it djangoplicity-actions-web futurize --stage1 -w -n .

futurize-stage2:
	docker exec -it djangoplicity-actions-web futurize --stage2 -w -n .