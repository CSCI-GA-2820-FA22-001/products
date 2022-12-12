"""
Product Service
Paths -- RESTful:
GET /products - Returns a list all of the Products
GET /products/{id} - Returns the Product with a given id number
POST /products - creates a new Product record in the database
PUT /products/{id} - updates a Product record in the database
DELETE /products/{id} - deletes a Product record in the database
"""

from flask import jsonify, request, url_for, abort,make_response
from service.models import Product
from service.common import status  # HTTP Status Codes
from . import app  # Import Flask application


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

######################################################################
# LIST ALL PRODUCTS
######################################################################
@app.route("/products", methods=["GET"])
def list_products():
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
    return jsonify(results), status.HTTP_200_OK

# ######################################################################
# # LIST ALL PRODUCTS BY NAME
# ######################################################################
# @app.route("/products/<string:product_name>/name", methods=["GET"])
# def list_products_by_name(product_name):
#     """Returns all of the Products by given name"""
#     app.logger.info("Request for Product list by given name")
#     products = []
#     products = Product.find_by_name(product_name)
#     results = [product.serialize() for product in products]
#     app.logger.info("Returning %d products", len(results))
#     return jsonify(results), status.HTTP_200_OK

# ######################################################################
# # LIST ALL PRODUCTS BY CATEGORY
# ######################################################################
# @app.route("/products/<string:product_category>/category", methods=["GET"])
# def list_products_by_category(product_category):
#     """Returns all of the Products by given category"""
#     app.logger.info("Request for Product list by given category")
#     products = []
#     products = Product.find_by_category(product_category)
#     results = [product.serialize() for product in products]
#     app.logger.info("Returning %d products", len(results))
#     return jsonify(results), status.HTTP_200_OK

# ######################################################################
# # LIST ALL PRODUCTS BY PRICE RANGE
# ######################################################################
# @app.route("/products/<string:product_range>/range", methods=["GET"])
# def list_products_by_price_range(product_range):
#     """Returns all of the Products by given price range"""
#     app.logger.info("Request for Product list by given range")
#     products = []
#     low, high = product_range.split("_")
#     products = Product.find_by_price_range(low, high)
#     results = [product.serialize() for product in products]
#     app.logger.info("Returning %d products", len(results))
#     return jsonify(results), status.HTTP_200_OK

######################################################################
# RETRIEVE A PRODUCT
######################################################################
@app.route("/products/<int:product_id>", methods=["GET"])
def get_products(product_id):
    """
    Retrieve a single Product
    This endpoint will return a Product based on it's id
    """

    app.logger.info("Request for product with id: %s", product_id)
    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found.")

    app.logger.info("Returning product: %s", product.name)
    return jsonify(product.serialize()), status.HTTP_200_OK

######################################################################
# ADD A NEW PRODUCT
######################################################################
@app.route("/products", methods=["POST"])
def create_products():
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
    location_url = url_for("get_products", product_id =product.id, _external=True)

    app.logger.info("Product with ID [%s] created.", product.id)
    return jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}

######################################################################
# DELETE A PRODUCT
######################################################################
@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_products(product_id):
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
@app.route("/products/<int:product_id>", methods=["PUT"])
def update_products(product_id):
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
    return jsonify(product.serialize()), status.HTTP_200_OK

######################################################################
# LIKE A PRODUCT
######################################################################
@app.route("/products/<int:product_id>/like", methods=["PUT"])
def like_products(product_id):
    """Like a Product makes it Likes Count Increment 1"""
    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found.")
    app.logger.info("Request to like product with id: %s", product_id)
    app.logger.info("Request to like product with like count: %s", product.like)
    product.like += 1
    product.update()
    return jsonify(product.serialize()), status.HTTP_200_OK
