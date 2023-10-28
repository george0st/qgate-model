rem Setting based on 'https://coverage.readthedocs.io/en/7.3.2/'

coverage erase
coverage run -m unittest discover
coverage combine
coverage report -m
coverage-badge -f -o coverage.svg
