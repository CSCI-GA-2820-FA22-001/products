"""
Product Service

Paths -- RESTful
"""
import sys
import secrets
import logging
from functools import wraps
from flask import Flask, jsonify, request, url_for, make_response, render_template, abort
from flask_restx import Api, Resource, fields, reqparse, inputs
from service.models import Product, DataValidationError, DatabaseConnectionError
from .common import status  # HTTP Status Codes


# Import Flask application
from . import app


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    return (
        "Reminder: return some useful information in json format about the service here",
        status.HTTP_200_OK,
    )


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def init_db():
    """ Initializes the SQLAlchemy app """
    global app
    YourResourceModel.init_db(app)
