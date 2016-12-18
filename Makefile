SHELL=/bin/bash
PROJECT_NAME=InstaCommander
MOD_NAME=instacommander
APP_ENTRY=bin/instacommander.py
TEST_CMD=SETTINGS=$$PWD/etc/testing.conf nosetests -w $(MOD_NAME)
TEST_DUMP="./maketests.log"

install:
	python setup.py install
	pip install ./wheelhouse/*

prototype:
	# ipython -i $(APP_ENTRY)
	python $(APP_ENTRY) $(username)

clean:
	rm -rf build dist *.egg-info
	-rm `find . -name "*.pyc"`
	find . -name "__pycache__" -delete

wheelhouse:
	python setup.py bdist_wheel

run:
	python $(APP_ENTRY)

shell:
	SETTINGS=$$PWD/etc/dev.conf bin/manage.py shell

watch:
	watchmedo shell-command -R -p "*.py" -c 'echo \\n\\n\\n\\nSTART; date; $(TEST_CMD) -c etc/nose/test-single.cfg; date' .

test:
	rm -f $(TEST_DUMP)
	$(TEST_CMD) -c etc/nose/test.cfg

single:
	$(TEST_CMD) -c etc/nose/test-single.cfg

build-wheels:
	pip wheel .
	pip wheel -r dependencies.txt

install-wheels:
	pip install --use-wheel --find-links=wheelhouse --no-index -r dependencies.txt

dependencies:
	pip freeze | sed '/$(PROJECT_NAME)/ d' > dependencies.txt

.PHONY: clean install test server watch db single docs shell dbshell wheelhouse prototype build-wheels install-wheels dependencies
