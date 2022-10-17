"""
Product Factory class for making fake objects
"""
import factory
from factory.fuzzy import FuzzyChoice
from service.models import Product


class ProductFactory(factory.Factory):
    """Creates fake products for test cases"""

    class Meta:
        model = Product

    id = factory.Sequence(lambda n: n)
    name = FuzzyChoice(choices=["iPhone", "iPad", "Macbook"])
    description = factory.Faker("word")
    price = FuzzyChoice(choices=[50, 100, 200])