__author__ = 'sam'
import unittest
from utils.sqlhelper import *
from models.CommonModel import *

class TestWineShop(unittest.TestCase):
    def test_sqlhelper(self):
        db = SqlHelper('wineshop')
        db.insert('test', [{'a': 1, 'b': 1}], ['a', 'b'])
        r = db.query_all('select * from test')
        self.assertEqual(len(r) >= 1, True)
        db.close()
    def test_common_model(self):
        class T(CommonModel):
            a = ''
            b = ''
        t = T({'a': 1, 'b': True})
        self.assertTrue('a' in t.all_field())
        self.assertEquals(t.a, 1)

if __name__ == '__main__':
    unittest.main()