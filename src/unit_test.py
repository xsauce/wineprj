from datetime import datetime
import uuid
from models.wineshop import Chateau

__author__ = 'sam'
import unittest
from models.CommonModel import DB

class TestWineShop(unittest.TestCase):
    def test_dal(self):
        DB.connect()
        c = Chateau.create(chateau_id=uuid.uuid4(), chateau_name='who', address='hello', geo='11,22', description='world', created_at=datetime.today())
        c.save()
        DB.close()

if __name__ == '__main__':
    unittest.main()