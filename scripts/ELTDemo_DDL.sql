sqlite3 --version

-- Create demo database
$ sqlite3 etldemo.db

$ .databases

$ DROP TABLE IF EXISTS Expenses;

$ CREATE TABLE Expenses
(
	date DATE,
	rate DECIMAL(8,6) NULL,
	USD DECIMAL(8,6) NULL,
	CAD DECIMAL(8,6) NULL
);

$ .tables

$ .exit

$ SELECT name, sql FROM sqlite_master
WHERE type='table'
ORDER BY name;

-- $ SELECT * FROM Expenses;
