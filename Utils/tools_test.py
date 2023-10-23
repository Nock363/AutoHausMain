import unittest
from tools import dictValuesToString, compareDictsByKeys

class TestTools(unittest.TestCase):
    
    def test_compareDictsByKeys(self):
        dictA = {
            "name": "John",
            "age": 30,
            "city": "New York",
            "subDict": {"a":20,"b":"hello","c":{"ca":20.0,"cb":"world"}}
        }
        dictB = {
            "name": "John",
            "age": 30,
            "city": "New York",
            "subDict": {"a":20,"b":"hello","c":{"ca":50.0,"cb":"bibboob"}}
        }
        self.assertTrue(compareDictsByKeys(dictA, dictB))

        dictC = {
            "name": "John",
            "age": 30,
            "city": "New York",
            "subDict": {"a":20,"b":"hello","c":20.0}
        }
        dictD = {
            "name": "John",
            "test": 40,
            "city": "New York",
            "subDict": {"a":50,"b":"world"}
        }
        self.assertFalse(compareDictsByKeys(dictC, dictD))

if __name__ == '__main__':
    unittest.main()
