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

    def test_create_a_product(self):
        """ It should Create a product and assert that it exists """
        product = Product(name = 'iphone', price = 50, description = 'this is iphone')
        self.assertTrue(product != None)
        self.assertEqual(product.id, None)
        self.assertEqual(product.name, 'iphone')
        self.assertEqual(product.price,50)
        self.assertEqual(product.description, "this is iphone")


