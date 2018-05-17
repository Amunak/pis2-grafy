all: init clean run

init:
	pip install -r requirements.txt

run:
	python -m pis2grafy

clean:
	rm output/*