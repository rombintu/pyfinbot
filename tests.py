import unittest

from internal import database
from tools import validator


class Test_Database_In_Memory(unittest.TestCase):
    db = database.Database("sqlite://", True)
    def test_create_note(self):
        note = validator.filter_by_input("100 food")
        ok, err = self.db.create_one(database.Note(
            uuid=213123123,
            cost=note["cost"],
            category=note["category"],
            comment=note["comment"]
            )
        )
        print(f"ERROR: {err}")
        self.assertEqual(ok, True)
    # def test_get_note(self):
    #     notes, err = self.db.get_last_week(213123123)
    #     print(f"OUTPUT:{notes}\nERROR: {err}")

    def test_get_note_by_week(self):
        notes, err = self.db.get_notes_by_days_ago(213123123, 10)
        print(f"ERROR: {err}")
        print(f"NOTES: {notes}")

if __name__ == '__main__':
    unittest.main()
