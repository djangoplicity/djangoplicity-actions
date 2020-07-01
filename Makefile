bash:
	docker exec -it djangoplicity-actions-web bash

test:
	docker exec -it djangoplicity-actions-web coverage run --source='.' manage.py test

coverage-html:
	docker exec -it djangoplicity-actions-web coverage html
	open ./htmlcov/index.html

test-python27:
	docker exec -it djangoplicity-actions-web tox -e py27-django111