bash:
	docker exec -it djangoplicity-actions-web bash

test:
	docker exec -it djangoplicity-actions-web coverage run --source='.' manage.py test

coverage-html:
	docker exec -it djangoplicity-actions-web coverage html
	google-chrome htmlcov/index.html

test-python27:
	docker exec -it djangoplicity-actions-web tox -e py27-django111

futurize-stage1:
	docker exec -it djangoplicity-actions-web futurize --stage1 -w -n .