# coding: utf-8
import datetime
from peewee import PrimaryKeyField, CharField, TextField, DateTimeField, ForeignKeyField, IntegerField, FloatField
from models.CommonModel import BaseModel, UUIDField, TimeStampField, CacheModel

__author__ = 'sam'


class OrderState(CacheModel):
    __objname__ = 'order_state'


class ProductLabel(CacheModel):
    __objname__ = 'product_label'


class WineSort(CacheModel):
    __objname__ = 'wine_sort'


class Brand(CacheModel):
    __objname__ = 'brand'


class Country(CacheModel):
    __objname__ = 'country'


class Region(CacheModel):
    __objname__ = 'region'


class GrapeSort(CacheModel):
    __objname__ = 'grape_sort'


class WineLevel(CacheModel):
    __objname__ = 'wine_level'


class Scene(CacheModel):
    __objname__ = 'scene'


class PostPlace(CacheModel):
    __objname__ = 'post_place'


class PaySort(CacheModel):
    __objname__ = 'pay_sort'


class ReceiptSort(CacheModel):
    __objname__ = 'receipt_sort'

class ReceiptContent(CacheModel):
    __objname__ = 'receipt_content'

class ShipCity(CacheModel):
    __objname__ = 'address'

class Shop(BaseModel):
    shop_id = UUIDField(primary_key=True)
    shop_name = CharField(max_length=100, null=False)
    address = CharField(max_length=200, null=False)
    geo = CharField(max_length=50, null=False)
    description = TextField(null=False)
    created_at = DateTimeField()
    updated_at = TimeStampField()


class ShopPhoto(BaseModel):
    photo_id = PrimaryKeyField()
    hash_value = CharField(max_length=50)
    shop = ForeignKeyField(Shop, related_name='photos')
    photo_type = CharField(max_length=10)


class User(BaseModel):
    uid = UUIDField(primary_key=True, null=False)
    username = CharField(max_length=100, null=False)
    password = CharField(max_length=50, null=False)
    email = CharField(max_length=50, null=False)
    phone = CharField(max_length=20, default=None)
    avatar = CharField(max_length=50, default=None)
    created_at = DateTimeField(null=False, default='NOW()')
    updated_at = TimeStampField(null=False)


class Administrator(BaseModel):
    aid = PrimaryKeyField()
    username = CharField(max_length=100, null=False)
    password = CharField(max_length=50, null=False)
    email = CharField(max_length=50, null=False)
    phone = CharField(max_length=20, null=False)
    created_at = DateTimeField(null=False)
    updated_at = TimeStampField(null=False)


class Product(BaseModel):
    pid = UUIDField(primary_key=True)
    name = CharField(max_length=100)
    description = TextField()
    volume = IntegerField()
    price = FloatField()
    shop = ForeignKeyField(Shop, related_name='products')
    brand = CharField(max_length=20, choices=Brand.choices())
    country = CharField(max_length=20, choices=Country.choices())
    region = CharField(max_length=20, choices=Region.choices())
    grape_sort = CharField(max_length=20, choices=GrapeSort.choices())
    wine_level = CharField(max_length=20, choices=WineLevel.choices())
    sort = CharField(max_length=20, choices=WineSort.choices())
    created_at = DateTimeField(null=False)
    updated_at = TimeStampField(null=False)


class ProductLabelList(BaseModel):
    pll_id = PrimaryKeyField()
    product = ForeignKeyField(Product, related_name='labels')
    label = CharField(max_length=10, choices=ProductLabel.choices())


class ProductSceneList(BaseModel):
    psl_id = PrimaryKeyField()
    product = ForeignKeyField(Product, related_name='scenes')
    scene = CharField(max_length=10, choices=Scene.choices())


class ProductPhoto(BaseModel):
    photo_id = PrimaryKeyField()
    hash_value = CharField(max_length=50)
    seq_num = IntegerField(null=False)
    photo_type = CharField(max_length=10, null=False)
    product = ForeignKeyField(Product, related_name='photos')
    created_at = DateTimeField(null=False)
    updated_at = TimeStampField(null=False)


class Repertory(BaseModel):
    repertory_id = PrimaryKeyField()
    product = ForeignKeyField(Product, related_name='repertory')
    sale_count = IntegerField(null=False, default=0)
    store_count = IntegerField(null=False, default=0)
    created_at = DateTimeField(null=False, default='NOW()')
    updated_at = TimeStampField(null=False)

    # @classmethod
    # def sale_product(cls, pid, product_count):
    #     sql = 'update %s set sale_count=sale_count+%s, store_count=store_count-%s where pid=%s' % (
    #         cls.__tablename__, product_count, product_count, pid
    #     )
    #     SqlHelper().execute(sql, {})
    #
    # @classmethod
    # def sale_product_for_batch(cls, pid_list_with_count):
    #     '''
    #     pid_list_with_count:data structure: {'pid': 113213, 'product_count':2 }
    #     '''
    #     sql = 'update ' + cls.__tablename__ + ' set sale_count=sale_count+%(product_count)s, store_count=store_count-%(product_count)s where pid=%(pid)s'
    #     SqlHelper().execute_many(sql, pid_list_with_count)


class RepertoryEntry(BaseModel):
    reid = PrimaryKeyField()
    product = ForeignKeyField(Product, related_name='repertory_entry')
    entry_count = IntegerField(null=False)
    created_at = DateTimeField(null=False)
    updated_at = TimeStampField(null=False)


class SaleOrder(BaseModel):
    # @classmethod
    # def get_order_state_num(cls, choice):
    #     return cls.choice_digitalize(choice, choice_list_name='ORDER_STATE_CHOICES')
    #
    # @classmethod
    # def get_order_state_display(cls, num):
    #     return cls.choice_display(num, choice_list_name='ORDER_STATE_CHOICES')
    soid = UUIDField(primary_key=True)
    user = ForeignKeyField(User, related_name='orders')
    addr_level1 = CharField(max_length=20, null=False)
    addr_level2 = CharField(max_length=20, null=False)
    addr_level3 = CharField(max_length=100, null=False)
    shipping_cost = FloatField(null=False, default=0.0)
    receiver = CharField(max_length=20, null=False)
    phone = CharField(max_length=20, null=False)
    receipt_sort = CharField(max_length=2, choices=ReceiptSort.choices())
    receipt_content = CharField(max_length=20)
    receipt_title = CharField(max_length=100)
    pay_sort = CharField(max_length=2, choices=PaySort.choices())
    order_state = CharField(max_length=2, choices=OrderState.choices())
    created_at = DateTimeField(null=False, default='NOW()')
    updated_at = TimeStampField(null=False)


class SaleOrderDetail(BaseModel):
    sod_id = UUIDField(primary_key=True)
    sale_order = ForeignKeyField(SaleOrder, related_name='detail')
    product = ForeignKeyField(Product, related_name='sale_order')
    purchase_count = IntegerField(null=False)
    price = FloatField(null=False)


class SaleOrderTrace(BaseModel):
    sot_id = UUIDField(primary_key=True)
    sale_order = ForeignKeyField(SaleOrder, related_name='trace')
    state = CharField(max_length=2, choices=OrderState.choices())
    created_at = DateTimeField(null=False)
    updated_at = TimeStampField(null=False)


class Poster(BaseModel):
    poster_id = PrimaryKeyField()
    hash_value = CharField(max_length=50, null=False)
    description = CharField(max_length=100)
    place = CharField(max_length=10, choices=PostPlace.choices(), null=False)
    pic_type = CharField(max_length=10, null=False)
    seq = IntegerField()
