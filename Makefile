.PHONY: docs

install-dev:
	pip install -e ".[dev,web]"

install-pre-commit:
	pre-commit install

style:
	pre-commit run --all-files

unit-test:
	pytest -m "not integration"

doc-test:
	PYTEST_PLUGINS=tests.common_fixtures pytest --doctest-modules sqlmesh/core sqlmesh/utils

core-it-test:
	pytest -m "core_integration"

it-test: core-it-test airflow-it-test-with-env

test: unit-test it-test doc-test

airflow-init:
	export AIRFLOW_ENGINE_OPERATOR=spark && make -C ./example/airflow init

airflow-run:
	make -C ./example/airflow run

airflow-stop:
	make -C ./example/airflow stop

airflow-clean:
	make -C ./example/airflow clean

airflow-psql:
	make -C ./example/airflow psql

airflow-spark-sql:
	make -C ./example/airflow spark-sql

airflow-it-test:
	export AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@localhost/airflow && \
		pytest -m "airflow_integration"

airflow-it-test-with-env: airflow-clean airflow-init airflow-run airflow-it-test airflow-stop

docs:
	pdoc/cli.py -o docs

docs-serve:
	pdoc/cli.py

web-serve:
	uvicorn web.main:app --port 8000 --reload
