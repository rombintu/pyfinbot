run:
	python3 main.py
test:
	python3 tests.py
backup:
	sqlite3 db.sqlite3 .dump > backup.sql