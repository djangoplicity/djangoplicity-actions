bash:
	docker exec -it djangoplicity-actions-web-3 bash

test:
	docker exec -it djangoplicity-actions-web-3 coverage run --source='.' manage.py test

coverage-html:
	docker exec -it djangoplicity-actions-web-3 coverage html
	google-chrome htmlcov/index.html

test-python27:
	docker exec -it djangoplicity-actions-web-3 tox -e py27-django111

futurize-stage1:
	docker exec -it djangoplicity-actions-web-3 futurize --stage1 -w -n .

futurize-stage2:
	docker exec -it djangoplicity-actions-web-3 futurize --stage2 -w -n .