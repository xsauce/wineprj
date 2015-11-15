__author__ = 'sam'
from CommonModel import *

class Product(CommonModel):
    name = Field()
    country = Field()
    region = Field()
    factory = Field()
    price = Field()
    description = Field()
