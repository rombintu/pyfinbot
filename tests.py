import unittest

from internal import database
from tools import validator


class Test_Database_In_Memory(unittest.TestCase):
    db = database.Database("sqlite://", True)
    def test_create_note(self):
        note = validator.filter_by_input("100к$ food")
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

    def test_get_note_last_month(self):
        notes, err = self.db.get_notes(213123123)
        print(f"ERROR: {err}")
        print(f"NOTES: {notes}")

    def test_get_note_curr_month(self):
        notes, err = self.db.get_notes(213123123, scope="current_month")
        print(f"ERROR: {err}")
        print(f"NOTES: {notes}")

if __name__ == '__main__':
    unittest.main()
