"""
Test cases for Product Model
"""
from itertools import product
import os
import logging
from pydoc import describe
import unittest
from sqlite3 import InternalError
from unicodedata import category, name
from unittest import TestCase
from unittest.mock import MagicMock, patch
from requests import HTTPError, ConnectionError
from sqlalchemy import null
from werkzeug.exceptions import NotFound
from service.models import Product, DataValidationError, db, DatabaseConnectionError
from service import app
from tests.factories import ProductFactory


DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)


######################################################################
#  P R O D U C T   M O D E L   T E S T   C A S E S
######################################################################
class TestProductModel(unittest.TestCase):
    """ Test Cases for Product Model """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Product.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.drop_all()  # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_read_a_product(self):
        """ It should Read a Product """
        product = ProductFactory()
        logging.debug(product)
        product.id = None
        product.create()
        self.assertIsNotNone(product.id)
        # Fetch it back
        found_product = Product.find(product.id)
        self.assertEqual(found_product.id, product.id)
        self.assertEqual(found_product.name, product.name)
        self.assertEqual(found_product.price, product.price)
        self.assertTrue(True)

    def test_get_all_products(self):
        """It should Get a list of all the Products"""
        products = Product.all()
        self.assertEqual(products, [])
        # Create 5 Products
        for _ in range(5):
            pet = ProductFactory()
            pet.create()
        # See if we get back 5 products
        products = Product.all()
        self.assertEqual(len(products), 5)

    def test_find_product(self):
        """ It should always be true """
        products = ProductFactory.create_batch(3)
        for product in products:
            product.create()
        logging.debug(products)

        self.assertEqual(len(Product.all()), 3)

        # Fetch it back
        product = Product.find(products[2].id)
        self.assertIsNot(product, None)
        self.assertEqual(product.id, products[2].id)
        self.assertEqual(product.name, products[2].name)
        self.assertEqual(product.price, products[2].price)
    
    def test_find_by_name(self):
        """It should Find a Product by Name"""
        products = ProductFactory.create_batch(3)
        for product in products:
            product.create()
        name = products[1].name
        count_name = 0
        for product in products:
            if product.name == name:
                count_name += 1
        found_products = Product.find_by_name(name)
        self.assertEqual(found_products.count(), count_name)
        self.assertEqual(found_products[0].name, products[1].name)
        # self.assertEqual(found_products[0].price, products[1].price)

    def test_find_or_404_found(self):
        """It should Find or return 404 not found"""
        products = ProductFactory.create_batch(3)
        for product in products:
            product.create()

        product = Product.find_or_404(products[1].id)
        self.assertIsNot(product, None)
        self.assertEqual(product.id, products[1].id)
        self.assertEqual(product.name, products[1].name)
        self.assertEqual(product.price, products[1].price)
    
    def test_find_or_404_not_found(self):
        """It should return 404 not found"""
        self.assertRaises(NotFound, Product.find_or_404, 0)
    
    def test_create_a_product(self):
        """ It should Create a product and assert that it exists """
        product = Product(name = "iphone", price = 50, description = 'this is iphone')
        self.assertEqual(str(product), "<Product 'iphone' id=[None]>")
        self.assertTrue(product != None)
        self.assertEqual(product.id, None)
        self.assertEqual(product.name, 'iphone')
        self.assertEqual(product.price,50)
        self.assertEqual(product.description, "this is iphone")
        product = Product(name = "iphone", price = 60, description = 'this is two iphone')
        self.assertEqual(product.price,60)
        self.assertEqual(product.description, "this is two iphone")
    
    def test_add_a_product(self):
        """It should Create a product and add it to the database"""
        products = Product.all()
        self.assertEqual(products, [])
        product = Product(name = "iphone", price = 50, description = 'this is iphone')
        self.assertTrue(product is not None)
        self.assertEqual(product.id, None)
        product.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(product.id)
        products = Product.all()
        self.assertEqual(len(products), 1)
        
    def test_update_a_product(self):
        """It should Update an existing Product"""
        product = ProductFactory()
        logging.debug(product)
        product.create()
        logging.debug(product)
        self.assertIsNotNone(product.id)
        # Change it an save it
        product.price = 100
        original_id = product.id
        product.update()
        self.assertEqual(product.id, original_id)
        self.assertEqual(product.price, 100)
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        products = Product.all()
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].id, 1)
        self.assertEqual(products[0].price, 100)
