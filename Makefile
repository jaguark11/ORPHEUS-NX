.PHONY: install test demo api
install:
	python -m pip install -e ".[dev]"

test:
	pytest

demo:
	python -m orpheus_nx.cli demo --steps 900 --nodes 10

api:
	uvicorn orpheus_nx.api:app --host 0.0.0.0 --port 8000
