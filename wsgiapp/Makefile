run:
	FLASK_APP=wsgiapp.main:app python3 -m flask run

invoke:
	cat ./tests/index.json | apex invoke -L serverless_wsgi

deploy:
	apex deploy


