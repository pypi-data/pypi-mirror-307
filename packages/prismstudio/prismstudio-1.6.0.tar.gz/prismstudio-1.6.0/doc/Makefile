# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXAUTOGEN ?= sphinx-autogen
SPHINXBUILD   ?= sphinx-build
SPHINXMULTIBUILD   ?= python3 -m multiversion
SOURCEDIR     = source
BUILDDIR      = build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

html:
	rm -f build/html/index.html
	rm -f build/html/root_page.html
	PYTHONPATH=../ $(SPHINXAUTOGEN) -o source/3_contentguide/contentguide/1_reference/1.5_api_reference/api source/3_contentguide/contentguide/1_reference/1.5_api_reference/*.rst
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	cp -r source/login/* build/html
	mv build/html/index.html build/html/root_page.html
	mv build/html/login.html build/html/index.html

# Deployment Build
# prefix "version/{version-name}"
mult-deploy:
	@$(SPHINXMULTIBUILD) $(SPHINXOPTS) "$(SOURCEDIR)" "$(BUILDDIR)"
	ls build/versions | xargs -I % sh -c "sed -i 's/.*redirect_prefix.*//' build/versions/%/_static/js/config.js"
	ls build/versions | xargs -I % sh -c 'echo "\nexport const redirect_prefix = \"/%\"" >> build/versions/%/_static/js/config.js;'
	ls build/versions | xargs -I % sh -c 'cp -r source/login/* build/versions/%;'
	ls build/versions | xargs -I % sh -c 'mv build/versions/%/index.html build/versions/%/root_page.html'
	ls build/versions | xargs -I % sh -c 'mv build/versions/%/login.html build/versions/%/index.html'
	cp source/_templates/index.html build/versions/index.html

# Local development
# prefix "docs/build/version/{version-name}"
mult:
	@$(SPHINXMULTIBUILD) $(SPHINXOPTS) "$(SOURCEDIR)" "$(BUILDDIR)"
	ls build/versions | xargs -I % sh -c "sed -i 's/.*redirect_prefix.*//' build/versions/%/_static/js/config.js"
	ls build/versions | xargs -I % sh -c 'echo "\nexport const redirect_prefix = \"/doc/build/versions/%\"" >> build/versions/%/_static/js/config.js;'
	ls build/versions | xargs -I % sh -c 'cp -r source/login/* build/versions/%;'
	ls build/versions | xargs -I % sh -c 'mv build/versions/%/index.html build/versions/%/root_page.html'
	ls build/versions | xargs -I % sh -c 'mv build/versions/%/login.html build/versions/%/index.html'
	cp source/_templates/index.html build/versions/index.html

# Local MAC development
# prefix "docs/build/version/{version-name}"
mac:
	@$(SPHINXMULTIBUILD) $(SPHINXOPTS) "$(SOURCEDIR)" "$(BUILDDIR)"
	ls build/versions | xargs -I % sh -c "sed -i '' 's/.*redirect_prefix.*//' build/versions/%/_static/js/config.js"
	ls build/versions | xargs -I % sh -c 'echo "\nexport const redirect_prefix = \"/doc/build/versions/%\"" >> build/versions/%/_static/js/config.js;'
	ls build/versions | xargs -I % sh -c 'cp -r source/login/* build/versions/%;'
	ls build/versions | xargs -I % sh -c 'mv build/versions/%/index.html build/versions/%/root_page.html'
	ls build/versions | xargs -I % sh -c 'mv build/versions/%/login.html build/versions/%/index.html'
	cp source/_templates/index.html build/versions/index.html

clean:
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	rm -rf source/3_contentguide/contentguide/1_reference/1.5_api_reference/api
