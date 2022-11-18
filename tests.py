import unittest

from internal import database
from tools import validator


class Test_Database_In_Memory(unittest.TestCase):
    db = database.Database("sqlite://", True)
    # db = database.Database("sqlite:///dbtest.sqlite3", False)
    def test_create_note(self):
        _note1 = validator.filter_by_input("100 food")
        note1 = database.Note(
            cost=_note1["cost"],
            category=_note1["category"],
            comment=_note1["comment"]
            )
        _note2 = validator.filter_by_input("200 lanch")
        note2 = database.Note(
            cost=_note2["cost"],
            category=_note2["category"],
            comment=_note2["comment"]
            )
        ok, err1 = self.db.create_note(100, note1)
        ok, err2 = self.db.create_note(200, note2)
        print(f"ERROR: {err1, err2}")
        self.assertEqual(ok, True)
    def test_get_note(self):
        notes1, err1 = self.db.get_notes(100, scope="current_month")
        print(f"OUTPUT USER 1:{notes1}\nERROR: {err1}")
        notes2, err2 = self.db.get_notes(200, scope="current_month")
        print(f"OUTPUT USER 2:{notes2}\nERROR: {err2}")

if __name__ == '__main__':
    unittest.main()
