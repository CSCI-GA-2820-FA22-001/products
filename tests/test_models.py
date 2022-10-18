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


    def test_update_a_product(self):
        """Update a Product"""
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