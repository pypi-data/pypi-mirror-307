# tests/test_core.py

import unittest
from wxswutilsapi import database
db = database('single.db')
class TestGreet(unittest.TestCase):
    def test_greet(self):
        db.query_table_with_time_diff('spectrum',"2024-11-06 10:40:00",20,30,{"plate_id":2},['id'])

if __name__ == '__main__':
    unittest.main()
