CURL ?= curl
ENVDIR ?= $(CURDIR)/env
MKDIR ?= mkdir -p
PIP = $(ENVDIR)/bin/pip
PYTHON = $(ENVDIR)/bin/python
STATEDIR = $(ENVDIR)/.state
TOUCH ?= touch
VIRTUALENV ?= pyvenv
# VIRTUALENV ?= virtualenv --quiet --prompt='{fluent-test}' --no-setuptools --no-pip

PIP_URL ?= https://raw.github.com/pypa/pip/master/contrib/get-pip.py
SETUPTOOLS_URL ?= https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py

REQUIREMENTS := $(STATEDIR)/requirements-installed $(STATEDIR)/test-requirements-installed $(STATEDIR)/tools-installed


.PHONY: environment

environment: $(ENVDIR) $(REQUIREMENTS)

$(STATEDIR)/requirements-installed: $(STATEDIR) requirements.txt
	$(PIP) install -qr requirements.txt
	@ $(TOUCH) "$@"

$(STATEDIR)/test-requirements-installed: $(STATEDIR) test-requirements.txt
	$(PIP) install -qr test-requirements.txt
	@ $(TOUCH) "$@"

$(STATEDIR)/tools-installed: $(STATEDIR) tools.txt
	$(PIP) install -qr tools.txt
	@ $(TOUCH) "$@"

$(ENVDIR):
	$(VIRTUALENV) $(ENVDIR)
	@ $(MKDIR) $(ENVDIR)/tmp
	@ cd $(ENVDIR)/tmp && $(CURL) -Ls -o- $(SETUPTOOLS_URL) | $(PYTHON)
	@ cd $(ENVDIR)/tmp && $(CURL) -Ls -o- $(PIP_URL) | $(PYTHON)
	@ $(RM) -r $(ENVDIR)/tmp
	@ $(MKDIR) $(STATEDIR)

$(STATEDIR): $(ENVDIR)
