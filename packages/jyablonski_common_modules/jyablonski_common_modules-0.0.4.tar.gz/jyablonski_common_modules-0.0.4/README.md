# jyablonski Common Modules
![Tests](https://github.com/jyablonski/jyablonski_common_modules/actions/workflows/test.yml/badge.svg) ![PyPI Deployment](https://github.com/jyablonski/jyablonski_common_modules/actions/workflows/deploy.yml/badge.svg) [![Coverage Status](https://coveralls.io/repos/github/jyablonski/jyablonski_common_modules/badge.svg?branch=master)](https://coveralls.io/github/jyablonski/jyablonski_common_modules?branch=master) ![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)

Version: 0.0.4

Small Repo used to maintain shared helper functions across my projects.

- PostgreSQL Connections + Upsert Functions
- General Python Functions
- Standard Logging & optional Opensearch Logging Functions
- AWS Helper Functions

## Testing
To run tests, run `make test`

## Install

#### Local
`poetry install --extras "es-logging"`
`poetry install --extras "all"

#### PyPi
`pip install jyablonski_common_modules`
`pip install jyablonski_common_modules[es-logging]`
`pip install jyablonski_common_modules[all]`