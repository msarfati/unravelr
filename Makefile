SHELL=/bin/bash
PROJECT_NAME=CypherCossack
DEV_CONFIG=$$PWD/etc/dev.conf
PRODUCTION_CONFIG=/etc/cypher_cossack.conf
CURRENT_CONFIG=$(DEV_CONFIG)
TEST_DUMP=./maketests.log
TESTING_CONFIG=$$PWD/etc/testing.conf
TEST_CMD=SETTINGS=$(TESTING_CONFIG) nosetests --verbosity=2 --where=./cypher_cossack/tests

install:
	python setup.py install

prototype:
	ipython -i bin/prototype.py

clean:
	rm -rf build dist *.egg-info
	-rm `find . -name "*.pyc"`
	find . -name "__pycache__" -delete

server:
	SETTINGS=$(CURRENT_CONFIG) bin/manage.py runserver

shell:
	SETTINGS=$(CURRENT_CONFIG) bin/manage.py shell

test:
	rm -f $(TEST_DUMP)
	$(TEST_CMD) 2>&1 | tee -a $(TEST_DUMP)

single:
	$(TEST_CMD) --attr=single

watch:
	watchmedo shell-command -R -p "*.py" -c 'echo \\n\\n\\n\\nSTART; date; $(TEST_CMD); date' .

wheelhouse:
	python setup.py bdist_wheel

build-wheels:
	pip wheel .
	pip wheel -r dependencies.txt

install-wheels:
	pip install --use-wheel --find-links=wheelhouse --no-index -r dependencies.txt

.PHONY: clean install test server watch single docs shell wheelhouse prototype build-wheels install-wheels