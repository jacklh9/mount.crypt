pip:
	pip install -r requirements.txt


conda:
	while read requirement; do conda install --yes $requirement; done < requirements.txt


both:
	while read requirement; do conda install --yes $requirement || pip install $requirement; done < requirements.txt


test:
	python3 tests/test_*.py


clean:
	if [ -e *~ ]; then \rm -i *~; fi
	if [ -e \#* ]; then \rm -i \#*; fi

.PHONY: clean conda pip


