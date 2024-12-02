#!/bin/bash

echo "Formatting code with Black..."
black src/ tests/ --config .code_quality/black.toml

echo "Sorting imports with isort..."
isort src/ tests/

echo "Code formatting complete!"