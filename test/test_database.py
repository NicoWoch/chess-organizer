import os.path
import unittest
from typing import Any

from src import database
from src.serializer import SetSerializer, TupleSerializer, Serializer

DATABASE_TMP_PATH = 'db.tmp.json'


class TestDatabase(unittest.TestCase):
    def test_file_creation(self):
        if os.path.isfile(DATABASE_TMP_PATH):
            os.remove(DATABASE_TMP_PATH)

        db = database.Database(DATABASE_TMP_PATH)
        db.read()

        self.assertTrue(os.path.isfile(DATABASE_TMP_PATH), 'Database does not created a db file')

    def __test_read_write(self, value: Any, *serializers: Serializer):
        db = database.Database(DATABASE_TMP_PATH, *serializers)
        db.write(value)
        red = db.read()

        self.assertEqual(value, red)
        self.assertEqual(type(value), type(red))

    def test_simple_types_1(self):
        self.__test_read_write(5)

    def test_simple_types_2(self):
        self.__test_read_write('hello world')

    def test_simple_types_3(self):
        self.__test_read_write([1, 4, 2, 3])

    def test_simple_types_4(self):
        self.__test_read_write({'x': 2, 'y': 3})

    def test_nested_types_1(self):
        self.__test_read_write({'x': 2, 'y': [1, 3, 2]})

    def test_nested_types_2(self):
        self.__test_read_write({'x': 2, 'y': [1, {}, 2]})

    def test_nested_types_3(self):
        self.__test_read_write({'x': [[[[2]], 1], [3]], 'y': [[[{'z': [5]}]], [], 2]})

    def test_custom_set_serializer_1(self):
        s = SetSerializer()
        self.__test_read_write({1, 2, 3}, s)

    def test_custom_set_serializer_2(self):
        s = SetSerializer()
        self.__test_read_write({'x': {1, 2, 'hi'}}, s)

    def test_custom_tuple_serializer_1(self):
        s = TupleSerializer()
        self.__test_read_write((1, 2), s)

    def test_custom_two_serializers_1(self):
        s1 = SetSerializer()
        s2 = TupleSerializer()
        self.__test_read_write({'x': {2, 1, 'hi'}, 'y': {1, 2, (3, 4)}, 'z': set()}, s1, s2)

    def test_custom_two_serializers_2(self):
        s1 = SetSerializer()
        s2 = TupleSerializer()
        self.__test_read_write([1, 2, {}, set(), (), (set(), 1, [set(), 4])], s1, s2)


if __name__ == '__main__':
    unittest.main()
