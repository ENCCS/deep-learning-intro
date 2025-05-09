# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = content
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile patch

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile patch
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

patch:
	python3 patch.py $(SOURCEDIR) episodes learners instructors profiles

# Live reload site documents for local development
livehtml:
	sphinx-autobuild \
		--pre-build "make patch" \
		--watch episodes --watch learners --watch instructors --watch profiles --watch patch.py \
		--ignore "$(SOURCEDIR)/_patched" \
		"$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
