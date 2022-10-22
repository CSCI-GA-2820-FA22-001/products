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
* URL <br>
  GET/products <br>
* Request Headers: NULL
* Body: NULL
* Success Response:
* Code: HTTP_200_OK
* Error Response: NULL

## Create a product
* URL <br>
  POST/products <br>
* Request Headers
* Body
* Success Response


## Delete a product
* URL <br>
  DELETE /products/<user_id>
* Request NULL
* Body NULL
* Success Response
  * **Code:** HTTP_204_NO_CONTENT <br />
    **Content:** 
    NO_CONTENT
## Read a product
* URL <br>
  GET /poducts/<product_id>
* Request NULL
* Body NULL
* Success Response
  * **Code:** HTTP_200_OK <br />
    **Content:** 
    ```json
    {
        "id": 2,
        "name" : "iphone",
        "price" : 50,
        "description" : "This is ihopne"
    }
    ```

