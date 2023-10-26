import unittest
from tools import dictValuesToString, compareDictsByKeys, isValidTimeFormat

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

    def test_isValidTimeFormat(self):

        correctTimeFormats = [
            "10:00:20",
            "22:00:20",
            "00:00:00",
        ]

        wrongTimeFormats = [
            "110",
            "11:000:20",
            "22:00:20:20",
            "22:00:10:20"
        ]

        for time in correctTimeFormats:
            print(f"checking correct time {time}")
            self.assertTrue(isValidTimeFormat(time))

        for time in wrongTimeFormats:
            print(f"checking wrong time {time}")
            self.assertFalse(isValidTimeFormat(time))

if __name__ == '__main__':
    unittest.main()
