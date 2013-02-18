# These targets are not files
.PHONY: contribute ci test i18n lint travis

install:
	python setup.py develop
	pip install -r requirements.txt