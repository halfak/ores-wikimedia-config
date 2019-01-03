REQUIREMENTS_FILES = \
	submodules/ores/requirements.txt \
	submodules/draftquality/requirements.txt \
	submodules/drafttopic/requirements.txt \
	submodules/editquality/requirements.txt \
	submodules/articlequality/requirements.txt \
	requirements.txt

OMIT_WHEELS = \
	ores \
	draftquality \
	drafttopic \
	editquality \
	articlequality \
	setuptools \
	pkg-resources

.DEFAULT_GOAL := all

all: clean_env deployment_wheels

clean_env:
	if [ -n "$$VIRTUAL_ENV" ]; then \
	  pip freeze | grep -v pip | xargs pip uninstall -y; \
	fi

pip_install:
	pip install wheel
	pip install --upgrade pip
	for req_txt in $(REQUIREMENTS_FILES); do \
	  pip install -r $$req_txt; \
	done

frozen-requirements.txt: pip_install
	pip freeze | \
	  grep -v $(addprefix -e , $(OMIT_WHEELS)) > \
	frozen-requirements.txt

deployment_wheels: frozen-requirements.txt
	mkdir -p wheels && \
	pip wheel -r frozen-requirements.txt -w wheels
