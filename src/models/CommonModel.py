__author__ = 'sam'

class Field():
    pass

class CommonModel(object):
    @classmethod
    def all_field(cls):
        return filter(lambda x: not x.startswith('__'), cls.__dict__.keys())

    def __init__(self, fields):
        for k, v in fields.items():
            if k in self.all_field():
                setattr(self, k, v)

class T(CommonModel):
    a = Field()
    b = Field()

