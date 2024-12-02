#!/bin/bash

echo "Linting code with Flake8..."
flake8 src/ tests/ --config .code_quality/flake8.ini

echo "Linting complete!"