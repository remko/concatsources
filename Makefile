.PHONY: check
check:
ifeq ($(COVERAGE),1)
	nosetests  --with-coverage
else
	nosetests
endif
