# NYU DevOps Project-Product

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)

This is the product services for NYU Devops fall 2022 E-commerce Project

## Run Code Instruction

To start the service.\
run command as follow in command line

```bash
    flask run
```

You Would Get these information in your browser

```
    {
        "name": "Product REST API Service", 
        "paths": "http://127.0.0.1:8000/products", 
        "version": "1.0"
    }
```

To run or test our service.\
run command as follow in command line

```bash
    nosetests
```

## Table Schema

```test
{
    id                Int           Primary key
    name              String          
    Price             Int
    Description       String
    Like              Int
}
```

## Rest API EndPoints

```
Product Service
Paths -- RESTful:
GET /products - Returns a list all of the Products
GET /products/{id} - Returns the Product with a given id number
POST /products - creates a new Product record in the database
PUT /products/{id} - updates a Product record in the database
DELETE /products/{id} - deletes a Product record in the database
```

## Get All products

## Create a product
* URL
  POST/products
* Request Headers
* Body
* Success Response
## Contents

The project contains the following:

```text
.gitignore          - this will ignore vagrant and other metadata files
.flaskenv           - Environment variables to configure Flask
.gitattributes      - File to gix Windows CRLF issues
.devcontainers/     - Folder with support for VSCode Remote Containers
dot-env-example     - copy to .env to use environment variables
requirements.txt    - list if Python libraries required by your code
config.py           - configuration parameters

service/                   - service python package
├── __init__.py            - package initializer
├── models.py              - module with business models
├── routes.py              - module with service routes
└── common                 - common code package
    ├── error_handlers.py  - HTTP error handling code
    ├── log_handlers.py    - logging setup code
    └── status.py          - HTTP status constants

tests/              - test cases package
├── __init__.py     - package initializer
├── test_models.py  - test suite for business models
└── test_routes.py  - test suite for service routes
```

## License

Copyright (c) John Rofrano. All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the NYU masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by *John Rofrano*, Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.
