"""
Test cases for Product Model
"""
from itertools import product
import os
import logging
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
        """ It should always be true """
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
