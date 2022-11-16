updatesql="""
BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS "users" (
	"id"	INTEGER NOT NULL UNIQUE,
	"first_name"	TEXT,
	"last_name"	TEXT,
	"username"	TEXT,
	"language_code"	BLOB,
	"chat"	NUMERIC,
	"coll"	INTEGER,
	"lastactive"	INTEGER,
	"lastsend"	INTEGER DEFAULT 0,
	PRIMARY KEY("id")
);

COMMIT;
"""
