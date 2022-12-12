"""
Models for Product

All of the models are stored in this module
"""
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint

logger = logging.getLogger("flask.app")

# add test for cicd pipline
# test 3
# test 4
# test 5
# 
# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()

def init_db(app):
    """Initialize the SQLAlchemy app"""
    Product.init_db(app)

class DatabaseConnectionError(Exception):
    """Custom Exception when database connection fails"""
    pass

class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """

    pass

class Product(db.Model):
    """
    Class that represents a Product
    """

    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63))
    price = db.Column(db.Integer, nullable=False, default=60)
    description = db.Column(db.String(256))
    like = db.Column(db.Integer, default=0)
    category = db.Column(db.String(63))
    def __repr__(self):
        return "<Product %r id=[%s]>" % (self.name, self.id)

    def create(self):
        """
        Creates a Product to the database
        """
        logger.info("Creating:%s", self.name)
        logger.info("Creating like count:%s",self.like)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a Product to the database
        """
        logger.info("Saving %s", self.name)
        logger.info("like count is %s", self.like)
        db.session.commit()

    def delete(self):
        """ Removes a Product from the data store """
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """Serializes a Product into a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "description": self.description,
            "like": self.like,
            "category": self.category
        }

    def deserialize(self, data):
        """
        Deserializes a Product from a dictionary

        Args:
            data (dict): A dictionary containing the Product data
        """
        try:
            name = data.get("name", "")
            self.category = data["category"]
            self.description = data["description"]
            # Check the validity of the price attribute
            price = data.get("price")

            like = data.get("like",0)

            if isinstance(like, int) or (isinstance(like, str) and like.isdigit()):
                self.like = int(like)
            else:
                raise DataValidationError(
                    "Invalid type for integer [like]: "
                    + str(type(data["like"]))
                )
            if int(like) >= 0:
                self.like= int(like)
            else:
                raise DataValidationError(
                    "Invalid value for price. Price should be a non-negative value"
                )

            if isinstance(price, int) or (price and price.isdigit()):
                self.price = int(price)
            else:
                raise DataValidationError(
                    "Invalid type for integer [price]: "
                    + str(type(data["price"]))
                )
            if int(price) >= 0:
                self.price = int(price)
            else:
                raise DataValidationError(
                    "Invalid value for price. Price should be a non-negative value"
                )
            if 0 < len(name) <= 20:
                self.name = name
            else:
                raise DataValidationError(
                    "Invalid value for name. Name length should between 1 - 20 characters."
                )
        # except AttributeError as error:
        #     raise DataValidationError("Invalid attribute: " + error.args[0]) from error
        except KeyError as error:
            raise DataValidationError("Invalid product: missing " + error.args[0]) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid product: body of request contained bad or no data" + str(error)
            )
        return self

    @classmethod
    def init_db(cls, app):
        """ Initializes the database session """
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """ Returns all of the Products in the database """
        logger.info("Processing all Products")
        return cls.query.all()

    @classmethod
    def find(cls, product_id: int):
        """Finds a Product by it's ID

        :param product_id: the id of the Product to find
        :type product_id: int

        :return: an instance with the product_id, or None if not found
        :rtype: Product

        """
        logger.info("Processing lookup for id %s ...", product_id)

        return cls.query.get(product_id)

    @classmethod
    def find_or_404(cls, product_id: int):
        """Find a Product by it's id

        :param product_id: the id of the Product to find
        :type product_id: int

        :return: an instance with the product_id, or 404_NOT_FOUND if not found
        :rtype: Product

        """
        logger.info("Processing lookup or 404 for id %s", product_id)
        return cls.query.get_or_404(product_id)

    @classmethod
    def find_by_name(cls, name: str) -> list:
        """Returns all Products with the given name

        :param name: the name of the Products you want to match
        :type name: str

        :return: a collection of Products with that name
        :rtype: list

        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)

    @classmethod
    def find_by_price_range(cls, lower_price: int, higher_price: int) -> list:
        """Returns all Products with the given price range

        :param lower_price: the lower bound of the Products price range you want to match
        :param higher_price: the higher bound of the Products price range you want to match
        :type lower_price, higher_price: int

        :return: a collection of Products with that range
        :rtype: list

        """
        logger.info("Processing price range query from %s to %s ...", lower_price, higher_price)
        return cls.query.filter(cls.price >= lower_price, cls.price <= higher_price)

    @classmethod    
    def find_by_category(cls, category: str) -> list:
        """Returns all Products with the given category
        :param category: the category of the Products you want to match
        :type category: str
        :return: a collection of Products with that category
        :type: list
        """
        
        logger.info("Processing name query for %s ...", category)
        return cls.query.filter(cls.category == category)

    # @classmethod
    # def find_by_price(cls, low: int, high: int) -> list:
    #     """Returns all Products with the given price range
    #     :param low: lower bound of the price range
    #     :param high: higher bound of the price range
    #     :return: a collection of Products within that price range
    #     :type: list
    #     """

    #     logger.info("Processing price query for price range between %i", low)
    #     return cls.query.filter(cls.price_range == (low, high))
