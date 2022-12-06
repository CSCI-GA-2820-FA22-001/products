"""
Product API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
from crypt import methods
import os
import logging
import json
import unittest
from unittest import TestCase
from unittest.mock import MagicMock, patch

from flask import url_for
from service import app
from service.models import db, init_db, Product
from service.common import status  # HTTP Status Codes
from tests.factories import ProductFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)
BASE_URL = "/products"


######################################################################
#  T E S T   C A S E S
######################################################################
class TestProductServer(TestCase):
    """ REST API Server Tests """

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        db.session.close()

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()
        db.session.query(Product).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()

    def _create_products(self, count):
        """Factory method to create products in bulk"""
        products = []
        for _ in range(count):
            test_product = ProductFactory()
            response = self.client.post(BASE_URL, json=test_product.serialize())
            self.assertEqual(
                response.status_code, status.HTTP_201_CREATED, "Could not create test products"
            )
            new_product = response.get_json()
            test_product.id = new_product["id"]
            products.append(test_product)
        return products
    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################


    def test_index(self):
        """ It should call the home page """
        response = self.client.get("/")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         data = response.get_json()
#         self.assertEqual(data["name"], "Product REST API Service")
#         self.assertEqual(data["version"], "1.0")
#         self.assertEqual(data["paths"],"http://localhost/products")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(b"Product Demo REST API Service", response.data)
        

    def test_health(self):
        """It should be healthy"""
        response = self.client.get("/healthcheck")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["status"], 200)
        self.assertEqual(data["message"], "Healthy")

    def test_get_product(self):
        """It should Get a single Product"""
        # get the id of a product
        test_product = self._create_products(1)[0]
        response = self.client.get(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["name"], test_product.name)
        self.assertEqual(data["price"], test_product.price)

    def test_get_product_not_found(self):
        """It should not Get a Product thats not found"""
        response = self.client.get(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        logging.debug("Response data = %s", data)
        self.assertIn("was not found", data["message"])

    def test_get_product_list(self):
        """It should Get a list of Products"""
        self._create_products(5)
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 5)
    
    def test_create_product(self):
        """It should Create a new Product"""
        test_product = ProductFactory()
        logging.debug("Test Product: %s", test_product.serialize())
        response = self.client.post(BASE_URL, json=test_product.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_product = response.get_json()
        self.assertEqual(new_product["name"], test_product.name)
        self.assertEqual(new_product["price"], test_product.price)
        self.assertEqual(new_product["description"], test_product.description)

        # Check that the location header was correct
        response = self.client.get(location)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_product = response.get_json()
        self.assertEqual(new_product["name"], test_product.name)
        self.assertEqual(new_product["price"], test_product.price)
        self.assertEqual(new_product["description"], test_product.description)


    def test_delete_product(self):
        """ It should Delete a Product """
        test_product = self._create_products(1)[0]
        response = self.client.delete(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(response.data), 0)
        response = self.client.get(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    
    


    def test_update_product(self):
        """It should Update an existing Product"""
        # create a product to update
        test_product = ProductFactory()
        response = self.client.post(BASE_URL, json=test_product.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # update the product
        new_product = response.get_json()
        logging.debug(new_product)
        new_product["price"] = 100
        response = self.client.put(f"{BASE_URL}/{new_product['id']}", json=new_product)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_product = response.get_json()
        self.assertEqual(updated_product["price"], 100)
    
    def test_update_a_non_exist_product(self):
        """It not should Update a Product that is not exist"""
        test_product = ProductFactory()
        response = self.client.post(BASE_URL, json=test_product.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # update the product
        new_product = response.get_json()
        logging.debug(new_product)
        new_product["price"] = 100
        response = self.client.put(f"{BASE_URL}/{new_product['id'] + 1}", json=new_product)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_product_negative_price(self):
        """ It should identify the price is invalid if price is negative """
        test_product = ProductFactory()
        logging.debug(test_product)

        test_product.price = -5
        response = self.client.post(BASE_URL, json = test_product.serialize())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_product_price_type_string(self):
        """ It should identify the price is invalid if price is not digit """
        test_product = ProductFactory()
        logging.debug(test_product)

        test_product.price = "s"
        response = self.client.post(BASE_URL, json = test_product.serialize())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_create_product_price_type_digit(self):
    #     """ It should identify the price is invalid if price is not digit """
    #     test_product = ProductFactory()
    #     logging.debug(test_product)

    #     test_product.price = "5"
    #     response = self.client.post(BASE_URL, json = test_product.serialize())
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_product_exceed_maxlength_name(self):
        """ It should identify the invalid name if name is not capitalized or exceed 20 characters"""
        test_product = ProductFactory()
        logging.debug(test_product)

        test_product.name = "Abcdefghijklmnopqrstuv"
        response = self.client.post(BASE_URL, json = test_product.serialize())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_product_no_data(self):
        """ It should not Create a Product with missing data """
        response = self.client.post(BASE_URL, json = {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_product_no_content_type(self):
        """ It should not Create a Product with no content type """
        response = self.client.post(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

   
# ----------------------------------------------------------
# TEST ACTION
# ----------------------------------------------------------
    def test_like_a_product(self):
        """It should Like a Product"""
        products = self._create_products(10)
        # available_pets = [pet for pet in pets if pet.available is True]
        product = products[0]
        old_like_count = product.like
        response = self.client.put(f"{BASE_URL}/{product.id}/like")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(f"{BASE_URL}/{product.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        logging.debug("Response data: %s", data)
        self.assertEqual(data["like"], old_like_count + 1)

        response = self.client.put(f"{BASE_URL}/{product.id}/like")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(f"{BASE_URL}/{product.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        logging.debug("Response data: %s", data)
        self.assertEqual(data["like"], old_like_count + 2)
    
    def test_like_a_non_exist_product(self):
        """It not should Like a Product that is not exist"""
        response = self.client.put(f"{BASE_URL}/{324232}/like")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
