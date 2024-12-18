#!/bin/bash

echo "Running Black..."
black src/ tests/ --config .code_quality/black.toml

echo "Running Flake8..."
flake8 src/ tests/ --config .code_quality/flake8.ini

echo "Running isort..."
isort src/ tests/ --settings-path .code_quality/isort.cfg

echo "Running MyPy..."
mypy src/ tests/ --config-file .code_quality/mypy.ini


echo "Code quality checks complete!"