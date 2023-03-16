test:
	python -m unittest date_entities/integration_tests.py
	# python -m unittest date_entities/add_entities_tests.py
	# python -m unittest date_entities/extraction_tests.py

try:
	python main.py --username jim --password *** --base_uri https://api.dev.documentcloud.org/api/ --auth_uri https://dev.squarelet.com/api/ --documents 10001757
