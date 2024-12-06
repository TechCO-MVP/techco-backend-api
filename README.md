# techco-backend-api

This project aims to be a robust, scalable, and serverless REST API built with Python and deployed on AWS, following clean code principles and best practices for maintainable software.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Code Quality](#code-quality)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## Features

- Serverless architecture using AWS Lambda
- RESTful API design
- Python 3.11 support
- Automated code formatting and linting
- Type checking with MyPy
- Unit testing with Pytest and coverage reports
- CI/CD pipelines with GitHub Actions

## Requirements

- Python 3.11
- Node.js and npm
- AWS CLI configured with appropriate credentials
- Poetry for dependency management

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/techco-backend-api.git
    cd techco-backend-api
    ```

2. Install dependencies:

    ```sh
    poetry install
    ```

3. Install serverless framework:

    ```sh
    npm install -g serverless
    npm install -g serverless-offline
    ```

## Usage

To start the serverless offline environment for local development:

```sh
sls offline
```

## Testing
Run the tests using Pytest:

```sh
poetry run pytest
```

Generate a coverage report:

```sh
poetry run pytest --cov=src tests/
```

## Code Quality
Run code quality checks:

```sh
chmod +x .code_quality/scripts/run_quality_checks.sh

.code_quality/scripts/run_quality_checks.sh
```

## Deployment
Deploy to the development environment:

```sh
sls deploy --stage dev
```

Deploy to the production environment:

```sh
sls deploy --stage prod
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/feature-name`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature-branch`)
6. Create a new Pull Request