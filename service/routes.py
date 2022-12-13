"""
Product Service
Paths -- RESTful:
GET /products - Returns a list all of the Products
GET /products/{id} - Returns the Product with a given id number
POST /products - creates a new Product record in the database
PUT /products/{id} - updates a Product record in the database
DELETE /products/{id} - deletes a Product record in the database
"""

# import sys
import secrets
# import logging
from functools import wraps
# from flask_restx import Api, Resource, fields, reqparse, inputs
# from flask import jsonify, request, url_for, abort,make_response
# from service.models import Product
# from service.common import status  # HTTP Status Codes
# from . import app, api # Import Flask application

from flask import jsonify, request, url_for, make_response, abort
from service.models import Product
from service.common import status  # HTTP Status Codes
from flask_restx import Api, Resource, fields, reqparse, inputs
from . import app  # Import Flask application
from werkzeug.exceptions import NotFound

######################################################################
# GET HEALTH CHECK
######################################################################
@app.route("/health")
def healthcheck():
    """Let them know our heart is still beating"""
    return jsonify(status=200, message="Healthy"), status.HTTP_200_OK


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    app.logger.info("Request for Root URL")
#     return (
#         jsonify(
#             name="Product REST API Service",
#             version="1.0",
#             paths=url_for("list_products", _external=True),
#         ),
#         status.HTTP_200_OK,
#     )
    return app.send_static_file("index.html")


api = Api(app,
          version='1.0.0',
          title='Product REST API Service',
          description='This is a Product server.',
          default='products',
          default_label='Product shop operations',
          doc='/apidocs', # default also could use doc='/apidocs/'
          prefix='/' # changed from /api to /
         )

# Define the model so that the docs reflect what can be sent
create_model = api.model('Product', 
{
    'name': fields.String(required=True,
                          description='The name of the Product'),
    'category': fields.String(required=True,
                              description='The category of Product (e.g., apple, phone, weapon, etc.)'),
    'price': fields.Integer(required=True,
                                description='The price of the Products.'),
    'description': fields.String(required=True,
                              description='The description of the Products'),
    'like': fields.Integer(required=True,
                                description='The number of likes the Products have.')
})

product_model = api.inherit(
    'ProductModel',
    create_model,
    {
        'id': fields.Integer(readOnly=True,
                            description='The unique id assigned internally by service'),
    }
)

# query string arguments
product_args = reqparse.RequestParser()
product_args.add_argument('name', type=str, location='args', required=False, help='List Products by name')
product_args.add_argument('category', type=str, location='args', required=False, help='List Products by category')
product_args.add_argument('price_range', type=str, location='args', required=False, help='List Products by price range')


######################################################################
#  PATH: /products
######################################################################
@api.route('/products', strict_slashes=False)
class ProductCollection(Resource):


    ######################################################################
    # LIST ALL PRODUCTS
    ######################################################################
    
    @api.doc('list_products')
    @api.expect(product_args, validate=True)
    @api.marshal_list_with(product_model)
    def get(self):
        """Returns all of the Products"""
        app.logger.info("Request for Product list")
        products = []

        category = request.args.get("category")
        name = request.args.get("name")
        price_range = request.args.get("price_range")

        if category:
            app.logger.info("Find by category: %s", category)
            products = Product.find_by_category(category)
        elif name:
            app.logger.info("Find by name: %s", name)
            products = Product.find_by_name(name)
        elif price_range:
            app.logger.info("Find by price range: %s", price_range)
            low, high = price_range.split("_")
            products = Product.find_by_price_range(int(low), int(high))
        else:
            app.logger.info("Find all")
            products = Product.all()

        results = [product.serialize() for product in products]
        app.logger.info("[%s] Products returned", len(results))
        return results, status.HTTP_200_OK

    ######################################################################
    # ADD A NEW PRODUCT
    ######################################################################
    
    @api.doc('create_products', security='apikey')
    @api.response(400, 'The posted data was not valid')
    @api.expect(create_model)
    @api.marshal_with(product_model, code=201)
    # @app.route("/products", methods=["POST"])
    # @token_required
    def post(self):
        """
        Creates a Products
        This endpoint will create a Products based the data in the body that is posted
        """
        app.logger.info("Request to create a product")
        check_content_type("application/json")
        product = Product()
        product.deserialize(request.get_json())
        product.create()
        message = product.serialize()
        location_url = api.url_for(ProductResource, product_id =product.id, _external=True)
        app.logger.info("Product with ID [%s] created.", product.id)
        return message, status.HTTP_201_CREATED, {"Location": location_url}



######################################################################
#  PATH: /products/{id}
######################################################################
@api.route('/products/<product_id>')
@api.param('product_id', 'The Product identifier')
class ProductResource(Resource):
    """
    ProductResource class
    Allows the manipulation of a single Product
    GET /product{id} - Returns a Product with the id
    PUT /product{id} - Update a Product with the id
    DELETE /product{id} -  Deletes a Product with the id
    """

    ######################################################################
    # RETRIEVE A PRODUCT
    ######################################################################
    
    @api.doc('get_products')
    @api.response(404, 'Product not found')
    @api.marshal_with(product_model)
    # @app.route("/products/<int:product_id>", methods=["GET"])
    def get(self, product_id):
        """
        Retrieve a single Product
        This endpoint will return a Product based on it's id
        """
        app.logger.info("Request for product with id: %s", product_id)
        product = Product.find(product_id)
        if not product:
            abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found.")
        app.logger.info("Returning product: %s", product.name)
        return product.serialize(), status.HTTP_200_OK


    ######################################################################
    # DELETE A PRODUCT
    ######################################################################
    @api.doc('delete_pets', security='apikey')
    @api.response(204, 'Pet deleted')
    # @token_required
    # @app.route("/products/<int:product_id>", methods=["DELETE"])
    def delete(self, product_id):
        """
        Delete a Product

        This endpoint will delete a Product based the id specified in the path
        """

        app.logger.info("Request to delete product with id: %s", product_id)

        product = Product.find(product_id)
        if product:
            product.delete()
        app.logger.info("Product with ID [%s] delete complete.", product_id) 
        return "", status.HTTP_204_NO_CONTENT


    ######################################################################
    # UPDATE AN EXISTING PRODUCT
    ######################################################################
    @api.doc('update_products', security='apikey')
    @api.response(404, 'Product not found')
    @api.response(400, 'The posted Product data was not valid')
    @api.expect(product_model)
    @api.marshal_with(product_model)
    # @token_required
    def put(self, product_id):
        """
        Update a Product

        This endpoint will update a Product based the body that is posted
        """
        app.logger.info("Request to update product with id: %s", product_id)
        check_content_type("application/json")

        product = Product.find(product_id)
        if not product:
            abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found.")
        origin_like = product.like
        product.deserialize(request.get_json())
        product.id = product_id
        product.like = origin_like
        product.update()

        app.logger.info("Product with ID [%s] updated.", product.id)
        return product.serialize(), status.HTTP_200_OK


######################################################################
#  PATH: /products/{id}/like
######################################################################
@api.route('/products/<product_id>/like')
@api.param('product_id', 'The Product identifier')
class LikeResource(Resource):

    ######################################################################
    # LIKE A PRODUCT
    ######################################################################
    @api.doc('like_products')
    # @api.response(404, 'Product not found')
    # @api.response(409, 'The Product is not available for purchase')
    # @app.route("/products/<int:product_id>/like", methods=["PUT"])
    def put(self, product_id):
        """Like a Product makes it Likes Count Increment 1"""
        product = Product.find(product_id)
        if not product:
            abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found.")
        app.logger.info("Request to like product with id: %s", product_id)
        app.logger.info("Request to like product with like count: %s", product.like)
        product.like += 1
        product.update()
        return product.serialize(), status.HTTP_200_OK
    


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def init_db():
    """ Initializes the SQLAlchemy app """
    global app
    Product.init_db(app)


def check_content_type(content_type):
    """Checks that the media type is correct"""
    if "Content-Type" not in request.headers:
        app.logger.error("No Content-Type specified.")
        abort(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Content-Type must be {content_type}",
        )

    if request.headers["Content-Type"] == content_type:
        return

    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {content_type}",
    )
